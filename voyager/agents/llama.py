# current model: llama-2-13b-chat
# """
# Sample usage:
# from llama import chat_completion
# response = chat_completion(messages)
# print(response)

import requests

from http import HTTPStatus
import json
import dashscope
from langchain.schema import AIMessage, HumanMessage, SystemMessage

with open("config.json", "r") as config_file:
    config = json.load(config_file)
def call_with_messages_server(msgs):
    url = f'http://{config["server_host"]}:{config["server_port"]}/llama2'
    input_msg = {
        "user_prompt": json.dumps(msgs[1].content),
        "system_prompt": json.dumps(msgs[0].content)
    }
    result = requests.post(url, json = input_msg)
    json_result = result.json()
    return AIMessage(content=json_result["data"])

def call_with_messages(msgs):
    dashscope.api_key = config["api_key"]  # API KEY
    messages = [{'role': 'system', 'content': msgs[0].content},
                {'role': 'user', 'content': msgs[1].content}
                ]
    response = dashscope.Generation.call(
        model='llama2-13b-chat-v2',
        messages=messages,
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        return AIMessage(content=response["output"]["choices"][0]["message"]["content"])
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
