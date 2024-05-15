import re
from voyager.prompts import load_prompt
from voyager.utils.json_utils import fix_and_parse_json
from langchain.schema import HumanMessage, SystemMessage
from voyager.agents.llama import call_with_messages

class CriticAgent:
    def __init__(
        self,
        model_name="gpt-3.5-turbo",
        temperature=0,
        request_timout=120,
        mode="auto",
    ):
        assert mode in ["auto", "manual"]
        self.mode = mode
        self.last_inventory = "Empty"
        self.last_inventory_used = 0

    def render_system_message(self):
        system_message = SystemMessage(content=load_prompt("critic"))
        return system_message

    def render_human_message(self, *, events, task, context, chest_observation):
        assert events[-1][0] == "observe", "Last event must be observe"
        biome = events[-1][1]["status"]["biome"]
        time_of_day = events[-1][1]["status"]["timeOfDay"]
        voxels = events[-1][1]["voxels"]
        health = events[-1][1]["status"]["health"]
        hunger = events[-1][1]["status"]["food"]
        position = events[-1][1]["status"]["position"]
        equipment = events[-1][1]["status"]["equipment"]
        inventory_used = events[-1][1]["status"]["inventoryUsed"]
        inventory = events[-1][1]["inventory"]

        for i, (event_type, event) in enumerate(events):
            if event_type == "onError":
                print(f"\033[31mCritic Agent: Error occurs {event['onError']}\033[0m")
                return None

        observation = ""

        # observation += f"Biome: {biome}\n\n"

        # observation += f"Time: {time_of_day}\n\n"

        # if voxels:
        #     observation += f"Nearby blocks: {', '.join(voxels)}\n\n"
        # else:
        #     observation += f"Nearby blocks: None\n\n"

        # observation += f"Health: {health:.1f}/20\n\n"
        # observation += f"Hunger: {hunger:.1f}/20\n\n"

        # observation += f"Position: x={position['x']:.1f}, y={position['y']:.1f}, z={position['z']:.1f}\n\n"
        observation += f"Task: {task}\n\n"
        observation += chest_observation

        observation += f"Equipment: {equipment}\n\n"

        if inventory:
            observation += f"Current Inventory ({inventory_used}/36): {inventory}\n\n"
        else:
            observation += f"Current Inventory ({inventory_used}/36): Empty\n\n"

        observation += f"Last inventory ({self.last_inventory_used}/36): {self.last_inventory}"

        self.last_inventory_used = inventory_used
        self.last_inventory = inventory

        for event_type, event in events:
            if event_type == 'onChat':
                chatlog = event['onChat']
        
        observation += f"Chat log: {chatlog}"
    
        # if context:
        #     observation += f"Context: {context}\n\n"
        # else:
        #     observation += f"Context: None\n\n"

        print(f"\033[31m****Critic Agent human message****\n{observation}\033[0m")
        return HumanMessage(content=observation)

    def human_check_task_success(self):
        confirmed = False
        success = False
        critique = ""
        while not confirmed:
            success = input("Success? (y/n)")
            success = success.lower() == "y"
            critique = input("Enter your critique:")
            print(f"Success: {success}\nCritique: {critique}")
            confirmed = input("Confirm? (y/n)") in ["y", ""]
        return success, critique

    def ai_check_task_success(self, messages, max_retries=5):
        if max_retries == 0:
            print(
                "\033[31mFailed to parse Critic Agent response. Consider updating your prompt.\033[0m"
            )
            return False, ""

        if messages[1] is None:
            return False, ""

        # critic = self.llm(messages).content
        # modify
        critic = call_with_messages(messages).content
        print(f"\033[31m****Critic Agent ai message****\n{critic}\033[0m")
        code_pattern = re.compile(r"{(.*?)}", re.DOTALL)
        code_name = "".join(code_pattern.findall(critic))
        critic = "{" + code_name + "}"
        try:
            response = fix_and_parse_json(critic)
            assert response["success"] in [True, False]
            if "critique" not in response:
                response["critique"] = ""
            return response["success"], response["critique"]
        except Exception as e:
            print(f"\033[31mError parsing critic response: {e} Trying again!\033[0m")
            return self.ai_check_task_success(
                messages=messages,
                max_retries=max_retries - 1,
            )

    def check_task_success(
        self, *, events, task, context, chest_observation, max_retries=5
    ):
        human_message = self.render_human_message(
            events=events,
            task=task,
            context=context,
            chest_observation=chest_observation,
        )

        messages = [
            self.render_system_message(),
            human_message,
        ]

        if self.mode == "manual":
            return self.human_check_task_success()
        elif self.mode == "auto":
            return self.ai_check_task_success(
                messages=messages, max_retries=max_retries
            )
        else:
            raise ValueError(f"Invalid critic agent mode: {self.mode}")

    def ai_check_goal_success(self, messages, max_retries=5):
        if max_retries == 0:
            print(
                "\033[31mFailed to parse Critic Agent response. Consider updating your prompt.\033[0m"
            )
            return False, ""

        if messages[1] is None:
            return False, ""

        # critic = self.llm(messages).content
        # modify
        critic = call_with_messages(messages).content
        print(f"\033[31m****Goal Agent ai message****\n{critic}\033[0m")
        code_pattern = re.compile(r"{(.*?)}", re.DOTALL)
        code_name = "".join(code_pattern.findall(critic))
        critic = "{" + code_name + "}"
        try:
            response = fix_and_parse_json(critic)
            assert response["success"] in [True, False]
            if "reasoning" not in response:
                response["reasoning"] = ""
            return response["reasoning"], response["success"]
        except Exception as e:
            print(f"\033[31mError parsing goal response: {e} Trying again!\033[0m")
            return self.ai_check_task_success(
                messages=messages,
                max_retries=max_retries - 1,
            )

    def check_goal_success(
        self, completed_task, failed_task, goals
    ):
        messages = [
            SystemMessage(content=load_prompt("goals")),
            HumanMessage(content=f"My completed task: {completed_task};\nMy failed task: {failed_task};\nMy ultimate goals: {goals}.\n")
        ]
        return self.ai_check_goal_success(messages=messages)