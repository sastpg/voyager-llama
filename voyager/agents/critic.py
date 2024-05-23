import re
from voyager.prompts import load_prompt
from voyager.utils.json_utils import fix_and_parse_json
from langchain.schema import HumanMessage, SystemMessage
from voyager.agents.llama import call_with_messages, ModelType

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

        if voxels:
            observation += f"Nearby blocks: {', '.join(voxels)}\n\n"
        else:
            observation += f"Nearby blocks: None\n\n"

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

        observation += f"Last inventory ({self.last_inventory_used}/36): {self.last_inventory}\n"

        self.last_inventory_used = inventory_used
        self.last_inventory = inventory

        chatlog = None
        for event_type, event in events:
            if event_type == 'onChat':
                chatlog = event['onChat']
                
        if chatlog:
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
        critic = call_with_messages(messages, ModelType.LLAMA2_70B).content
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
        # elif self.mode == 'pragram':
        #     return self.program_check_task_success(
        #         events=events, task=task
        #     )
        else:
            raise ValueError(f"Invalid critic agent mode: {self.mode}")
    
    def check_subgoal_success(self, events, task)->bool:
        inventory = self.get_inventory(events=events)
        if task == 'craft crafting table':
            return 'crafting_table' in inventory
        if task == 'craft wooden pickaxe':
            return 'wooden_pickaxe' in inventory
        if task == 'craft stone pickaxe':
            return 'stone_pickaxe' in inventory
        if task == 'craft iron pickaxe':
            return 'iron_pickaxe' in inventory
        if task == 'mine diamond':
            return 'diamond' in inventory
        

    def program_check_task_success(self, events, task)->bool:
        inventory = self.get_inventory(events=events)
        return task in inventory

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
    def get_inventory(self, events)->dict:
        assert events[-1][0] == "observe", "Last event must be observe"
        event = events[-1][1]
        inventory = event["inventory"]
        return inventory

    def render_observation(self, *, events, completed_tasks, failed_tasks):
        assert events[-1][0] == "observe", "Last event must be observe"
        event = events[-1][1]
        biome = event["status"]["biome"]
        time_of_day = event["status"]["timeOfDay"]
        voxels = event["voxels"]
        block_records = event["blockRecords"]
        entities = event["status"]["entities"]
        health = event["status"]["health"]
        hunger = event["status"]["food"]
        position = event["status"]["position"]
        equipment = event["status"]["equipment"]
        inventory_used = event["status"]["inventoryUsed"]
        inventory = event["inventory"]

        if not any(
            "dirt" in block
            or "log" in block
            or "grass" in block
            or "sand" in block
            or "snow" in block
            for block in voxels
        ):
            biome = "underground"

        other_blocks = ", ".join(
            list(
                set(block_records).difference(set(voxels).union(set(inventory.keys())))
            )
        )

        other_blocks = other_blocks if other_blocks else "None"

        nearby_entities = (
            ", ".join([k for k, v in sorted(entities.items(), key=lambda x: x[1])])
            if entities
            else "None"
        )

        completed_tasks = (
            ", ".join(completed_tasks) if completed_tasks else "None"
        )
        failed_tasks = ", ".join(failed_tasks) if failed_tasks else "None"

        observation = {
            "context": "",
            "biome": f"Biome: {biome}\n\n",
            "time": f"Time: {time_of_day}\n\n",
            "nearby_blocks": f"Nearby blocks: {', '.join(voxels) if voxels else 'None'}\n\n",
            "other_blocks": f"Other blocks that are recently seen: {other_blocks}\n\n",
            "nearby_entities": f"Nearby entities: {nearby_entities}\n\n",
            "health": f"Health: {health:.1f}/20\n\n",
            "hunger": f"Hunger: {hunger:.1f}/20\n\n",
            "position": f"Position: x={position['x']:.1f}, y={position['y']:.1f}, z={position['z']:.1f}\n\n",
            "equipment": f"Equipment: {equipment}\n\n",
            "inventory": f"Inventory ({inventory_used}/36): {inventory if inventory else 'Empty'}\n\n",
            "completed_tasks": f"Completed tasks so far: {completed_tasks}\n\n",
            "failed_tasks": f"Failed tasks that are too hard: {failed_tasks}\n\n",
        }
        return observation
    
    def check_goal_success(
        self, events, completed_task, failed_task, goals
    ):
        observations = self.render_observation(events=events, completed_tasks=completed_task, failed_tasks=failed_task)
        content = ''
        for key in observations:
            content += observations[key]
        content += f"My ultimate goals: {goals}"
        messages = [
            SystemMessage(content=load_prompt("goals")),
            HumanMessage(content=content)
        ]
        return self.ai_check_goal_success(messages=messages)