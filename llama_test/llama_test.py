# -*- coding: utf-8 -*-
import requests
from http import HTTPStatus
import dashscope
import os
import json
from langchain.schema import AIMessage, HumanMessage, SystemMessage

with open("config.json", "r") as config_file:
    config = json.load(config_file)
def call_with_messages(msgs):
    url = f'http://{config["server_host"]}:{config["server_port"]}/llama2'
    result = requests.post(url, json = msgs)
    return result.json()

with open("llama_test/combat_sys_prompt.txt", "r") as file:
    txt_content = file.read().strip()
json_content = json.dumps(txt_content)
msg1_content = json.loads(json_content)
msg2_content = "3 zombies."
test_msg = {
    "user_prompt": msg2_content,
    "system_prompt": msg1_content
   }
if __name__ == '__main__':
    # print(os.getcwd())
    # print(call_with_messages(f'system:{msg1_content}\n\nuser_prompt:{msg2_content}'))
    print(call_with_messages(test_msg))