import re
from voyager.prompts import load_prompt
from voyager.utils.json_utils import fix_and_parse_json
from langchain.schema import HumanMessage, SystemMessage
from voyager.agents.llama import call_with_messages

env_prompt = {
    'combat': 'combat_critic_prompt'
}

class CommentAgent:
    def __init__(
        self,
        environment,
        mode="auto",
    ):
        assert mode in ["auto", "manual"]
        self.env = environment
        self.mode = mode

    def render_system_message(self):
        system_message = SystemMessage(content=load_prompt(env_prompt[self.env]))
        return system_message

    def render_human_message(self, events, task_list, time_ticks, iteration):
        assert events[-1][0] == "observe", "Last event must be observe"
        health = events[-1][1]["status"]["health"]

        for i, (event_type, event) in enumerate(events):
            if event_type == "onError":
                print(f"\033[31mCritic Agent: Error occurs {event['onError']}\033[0m")
                return None

        observation = ""
        observation += f"Used Time: {time_ticks} ticks"
        observation += f"Toal iteration: {iteration}"
        observation += f"Task: {task_list}\n\n"
        for event in reversed(events):
            if event[0] == 'onChat':
                result = event[1]['onChat']
                break
        observation += f"Result: {result}"
        observation += f"Health: {health}"

        print(f"\033[31m****Critic Agent human message****\n{observation}\033[0m")
        return HumanMessage(content=observation)

    def human_check_task_success(self):
        confirmed = False
        critique = ""
        while not confirmed:
            reason = input("Reason:")
            critique = input("Enter your critique:")
            print(f"Reason: {reason}\nCritique: {critique}")
            confirmed = input("Confirm? (y/n)") in ["y", ""]
        return reason, critique

    def ai_check_task_success(self, messages, max_retries=5):
        if max_retries == 0:
            print(
                "\033[31mFailed to parse Critic Agent response. Consider updating your prompt.\033[0m"
            )
            return "", ""

        if messages[1] is None:
            return "", ""

        # modify
        critic = call_with_messages(messages).content
        print(f"\033[31m****Comment Agent ai message****\n{critic}\033[0m")
        code_pattern = re.compile(r"{(.*?)}", re.DOTALL)
        code_name = "".join(code_pattern.findall(critic))
        critic = "{" + code_name + "}"
        try:
            response = fix_and_parse_json(critic)
            # assert response["success"] in [True, False]
            if "reason" not in response:
                response["reason"] = ""
            if "critique" not in response:
                response["critique"] = ""
            return response["reason"], response["critique"]
        except Exception as e:
            print(f"\033[31mError parsing critic response: {e} Trying again!\033[0m")
            return self.ai_check_task_success(
                messages=messages,
                max_retries=max_retries - 1,
            )

    def check_task_success(
        self, *, events, task, time, iter, max_retries=5
    ):
        human_message = self.render_human_message(
            events=events,
            task_list=task,
            time_ticks=time,
            iteration=iter
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
            raise ValueError(f"Invalid comment agent mode: {self.mode}")
        