import os
import http
import dashscope
import json

with open('config.json', 'r') as f:
    config = json.load(f)

dashscope.api_key = config['api_key']

def call_llama(js_content):
    """
    call LLAMA for description generation.

    Args:
        js_content: javascript code

    Returns:
        str: LLAMA response
    """
    system_message = """I will provide you with a task code based on the mineflayer framework for Minecraft gameplay.
Please generate a brief description based on the content and comments of the provided JavaScript code.
Your response should start with "This function" and should not contain any additional information!"""
    messages = [{'role': 'system', 'content': system_message},
                {'role': 'user', 'content': js_content}]

    response = dashscope.Generation.call(
        model='qwen1.5-72b-chat',
        messages=messages,
        result_format='message'
    )

    if response.status_code == http.HTTPStatus.OK:
        description = response["output"]["choices"][0]["message"]["content"]
        print("Generated Description:", description)
        return description
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
        return None

def main(mode="all"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    code_dir = os.path.join(script_dir, "code")
    description_dir = os.path.join(script_dir, "description")

    for js_file in os.listdir(code_dir):
        if js_file.endswith(".js"):
            js_file_path = os.path.join(code_dir, js_file)
            description_file_path = os.path.join(description_dir, os.path.splitext(js_file)[0] + ".txt")

            if mode == "missing" and os.path.exists(description_file_path):
                print(f"Skipping {js_file} as description already exists")
                continue

            with open(js_file_path, 'r') as f:
                js_content = f.read()

            description = call_llama(js_content)

            if description:
                with open(description_file_path, 'w') as f:
                    f.write(description)
                    print(f"Description for {js_file} has been written to {description_file_path}")

if __name__ == "__main__":
    main(mode="all")  
    # mode "all" generates descriptions for all skills
    # mode "missing" generates descriptions for new skills
