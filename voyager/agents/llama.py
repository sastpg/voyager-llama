# current model: llama-2-13b-chat
# """
# Sample usage:
# from llama import chat_completion
# response = chat_completion(messages)
# print(response)

import requests

from http import HTTPStatus
import dashscope
from langchain.schema import AIMessage, HumanMessage, SystemMessage

def chat_completion(messages):
    url = 'http://10.214.211.106:8000/v1/chat/completions'
    result = requests.post(url, json = messages)
    return result.text

def call_with_messages(msgs):
    dashscope.api_key = 'sk-8386af4aa8d14cf8b9b7ca1250aabfdc'  # API KEY
    # dashscope.api_key = 'sk-eac17c70d6da479aba494487aca5907b'  
    messages = [{'role': 'system', 'content': msgs[0].content},
                {'role': 'user', 'content': msgs[1].content}
                ]
    response = dashscope.Generation.call(
        model=dashscope.Generation.Models.qwen_max,
        # model='llama2-13b-chat-v2',
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
