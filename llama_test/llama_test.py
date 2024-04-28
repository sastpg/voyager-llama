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
    url = f'http://{config["server_host"]}:{config["server_port"]}/llama'
    result = requests.post(url, json = msgs)
    return result.text

with open("llama_test/combat_sys_prompt.txt", "r") as file:
    msg1_content = file.read().strip()
test_msg = {
    "user_prompt": "10 minutes, 1 zombie.",
    "system_prompt": msg1_content
}
if __name__ == '__main__':
    # print(os.getcwd())
    print(call_with_messages(test_msg))