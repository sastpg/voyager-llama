# -*- coding: utf-8 -*-

from http import HTTPStatus
import dashscope
import os
from langchain.schema import AIMessage, HumanMessage, SystemMessage

def call_with_messages(msgs):
    dashscope.api_key = 'sk-eac17c70d6da479aba494487aca5907b'  # API KEY
    messages = [{'role': 'system', 'content': msgs[0].content},
                {'role': 'user', 'content': msgs[1].content}
                ]
    # print("input:", messages)
    response = dashscope.Generation.call(
        model='llama2-13b-chat-v2',
        messages=messages,
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        output_content = response["output"]["choices"][0]["message"]["content"]
        print("LLAMA Response Content:", output_content)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

with open("llama_test/construction_sys_prompt.txt", "r") as file:
    msg1_content = file.read().strip()
msg1 = SystemMessage(content=msg1_content)
msg2 = HumanMessage(content="A(328, 60, -147) B(337, 60, -138) Rails already laid: (328, 60, -147), (337, 60, -138)")
test_msg = [msg1, msg2]

if __name__ == '__main__':
    # print(os.getcwd())
    call_with_messages(test_msg)