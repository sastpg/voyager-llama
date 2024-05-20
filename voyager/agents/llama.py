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
from pathlib import Path
from voyager.utils import config
# with open(Path(__file__).parent.parent.parent / "conf/config.json", "r") as config_file:
#     config = json.load(config_file)
def call_with_messages(msgs):
    url = f'http://{config.get("server_host")}:{config.get("server_port")}/llama3_8b_v1'
    input_msg = {
        "user_prompt": msgs[1].content,
        "system_prompt": msgs[0].content
    }
    # print(input_msg)
    result = requests.post(url, json = input_msg)
    json_result = result.json()
    # print(json_result)
    return AIMessage(content=json_result["data"])

def call_with_messages_(msgs):
    dashscope.api_key = config.get("api_key")  # API KEY
    messages = [{'role': 'system', 'content': msgs[0].content},
                {'role': 'user', 'content': msgs[1].content}
                ]
    response = dashscope.Generation.call(
        model='llama3-8b-instruct',
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
