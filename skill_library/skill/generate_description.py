import os
import http
import dashscope

dashscope.api_key = 'sk-eac17c70d6da479aba494487aca5907b' # API KEY

def load_system_message():
    """
    load system message from sysMsg.txt.

    Returns:
        str: llama response.
    """
    sys_msg_file = "sysMsg.txt"
    if os.path.exists(sys_msg_file):
        with open(sys_msg_file, 'r') as f:
            return f.read()
    else:
        return ""

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
        model='llama2-13b-chat-v2',
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

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    code_dir = os.path.join(script_dir, "code")
    description_dir = os.path.join(script_dir, "description")

    for js_file in os.listdir(code_dir):
        if js_file.endswith(".js"):
            js_file_path = os.path.join(code_dir, js_file)
            description_file_path = os.path.join(description_dir, os.path.splitext(js_file)[0] + ".txt")

            with open(js_file_path, 'r') as f:
                js_content = f.read()

            description = call_llama(js_content)

            if description:
                with open(description_file_path, 'w') as f:
                    f.write(description)
                    print(f"Description for {js_file} has been written to {description_file_path}")

if __name__ == "__main__":
    main()
