# current model: llama-2-13b-chat
# """
# Sample usage:
# from llama import chat_completion
# response = chat_completion(messages)
# print(response)

# Sample response:
# onesix{"choices":[{"delta":{"content":"Ah, Hangzhou! The city of tea, silk, and beautiful West Lake. As a helpful assistant, I'd be happy to recommend some must-see attractions for your trip. Here are the top things to do and see in Hangzhou:

# 1. West Lake (Xi Hu): A stunning natural attraction and a popular destination for locals and tourists alike. Take a leisurely boat ride, hike along the scenic trails, or simply sit and enjoy the serene atmosphere.
# 2. Lingyin Temple: One of China's most famous Buddhist temples, Lingyin is adorned with intricate carvings, colorful paintings, and a 100-foot-tall pagoda. It's a great place to learn about Buddhist culture and history.
# 3. Longjing Tea Plantations: Hangzhou is famous for its green tea, and Longjing Tea Plantations are the perfect place to learn about tea production and taste some of the best tea in China.
# 4. Leifeng Pagoda: A five-story pagoda located on the south bank of West Lake, Leifeng Pagoda offers breathtaking views of the lake and surrounding hills.
# 5. Hefang Street: This bustling street is a shopper's paradise, filled with local snacks, souvenirs, and traditional Chinese medicine. It's a great place to experience the local culture and try some delicious street food.
# 6. Xixi National Wetland Park: A natural oasis in the heart of the city, Xixi National Wetland Park is home to a variety of wildlife and offers beautiful scenery and peaceful walks.
# 7. Songcheng Park: A large-scale cultural theme park that recreates the Song Dynasty (960-1279 AD) era of Hangzhou, Songcheng Park features traditional architecture, music, and performances.
# 8. Hangzhou Zoo: A popular destination for families, the Hangzhou Zoo is home to over 200 species of animals, including giant pandas, golden monkeys, and Asian elephants.
# 9. Qinghefang Ancient Street: A well-preserved historic street that dates back to the Qing Dynasty (1644-1911 AD), Qinghefang Ancient Street is lined with traditional shops, teahouses, and restaurants.
# 10. Xiang Hu Lake: A peaceful lake located in the north of Hangzhou, Xiang Hu Lake is surrounded by temples, gardens, and hiking trails, making it a great place for outdoor activities and relaxation.

# These are just a few of the many amazing attractions Hangzhou has to offer. Depending on your interests and preferences, there are plenty of other hidden gems to explore in this beautiful city. Have a wonderful trip!","role":"assistant"}}]}

# """

# import requests

# def chat_completion(messages):
#     url = 'http://10.214.211.106:8000/v1/chat/completions'
#     result = requests.post(url, json = messages)
#     return result.text


# if __name__ == '__main__':
#     example_messages = {"messages": [
#         {
#             "role": 'system',
#             "content": """You are a helpful assistant that generates a curriculum of subgoals to complete any Minecraft task specified by me.

# I'll give you a final task and my current inventory, you need to decompose the task into a list of subgoals based on my inventory.

# You must follow the following criteria:
# 1) Return a Python list of subgoals that can be completed in order to complete the specified task.
# 2) Each subgoal should follow a concise format, such as "Mine [quantity] [block]", "Craft [quantity] [item]", "Smelt [quantity] [item]", "Kill [quantity] [mob]", "Cook [quantity] [food]", "Equip [item]".
# 3) Include each level of necessary tools as a subgoal, such as wooden, stone, iron, diamond, etc.

# You should only respond in JSON format as described below:
# ["subgoal1", "subgoal2", "subgoal3", ...]
# Ensure the response can be parsed by Python `json.loads`, e.g.: no trailing commas, no single quotes, etc.""",
#         },
#         {
#             "role": 'user',
#             "content": """Inventory (1/36): {'oak_log': 1}""",
#         },
#         {
#             "role": 'user',
#             "content": 'Task: Mine 6 Wood Log'
#         },
#     ]
#     }
#     response = chat_completion(example_messages)
#     print(response)

from http import HTTPStatus
import dashscope
from langchain.schema import AIMessage, HumanMessage, SystemMessage

def call_with_messages(msgs):
    dashscope.api_key = 'sk-eac17c70d6da479aba494487aca5907b'  # API KEY
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


if __name__ == '__main__':
    message = [SystemMessage(content="""In Minecraft, breeding an animal requires first getting the corresponding animal.
For sheep, a pair of scissors can be made to cut the wool.
For cows, a bucket can be made to collect milk;
For chickens, the eggs can be collected;
For pigs, you can tame and ride them.
For any animal, it can be bred, killed, cooked and eaten.

I will give you information about the environment around you, that is, how many animals are each, in the format:
[[quantity] [type], ...]

You must generate your breeding plan following the following criteria:
1) Return a Python list of subgoals that can be completed in order to complete the specified task.
2) Each subgoal should follow a concise format "get/breed/kill [animal type]", "cook/eat [food type]" or some specific action "shear sheep" or "collect milk"

You should only respond in JSON format as described below:
["subgoal1", "subgoal2", "subgoal3", ...]
Ensure the response can be parsed by Python `json.loads`, e.g.: no trailing commas, no single quotes, etc."""), HumanMessage(content="[Three sheeps, two pigs]")]
    ai_msg = call_with_messages(message)
    print(ai_msg.content)