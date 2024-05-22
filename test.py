from voyager import Voyager
from voyager.utils import config
mc_port = config.get('MC_SERVER_PORT')
mc_host = config.get('MC_SERVER_HOST')
embedding_dir = config.get('SENTENT_EMBEDDING_DIR')

mc_host = "10.214.211.110"
mc_port = 25565
# mc_host = "127.0.0.1"
# mc_port = 49741 # local server
env_wait_ticks = 100
voyager = Voyager(
    mc_port=mc_port,
    mc_host=mc_host,
    env_wait_ticks=env_wait_ticks,
    skill_library_dir="./skill_library",
    reload=False, # set to True if the skill_json updated
    embedding_dir="D:\DESKTOP\paraphrase-multilingual-MiniLM-L12-v2", # your model path
    # embedding_dir="/home/MCagent/paraphrase-multilingual-MiniLM-L12-v2", # linux model path
    environment='combat'
)
mob_list = ["1 zombie", "1 skeleton",  "1 blaze", "1 zombified_piglin", "1 wither_skeleton"]
many_mob_list = [# "5 zombie", 
                 "1 zombie, 1 skeleton, 1 spider",
                 "3 skeleton", "5 skeleton"]
multi_mob_list = [# "1 zombie, 1 skeleton",
                  # "1 zombie, 1 spider",
                  "1 zombie, 1 skeleton, 1 spider"]
farming_task_list = ["plant 1 wheat seed and cook 1 meat (beef / mutton / pork / chicken)",
                     "collect 1 wool by shears and collect 1 bucket of milk",
                     "plant 1 melon seed and pumpkin seed",
                     # "plant 1 wheat seed", "plant 1 melon seed or pumpkin seed", "collect 1 wool by shears or collect 1 bucket of milk", 
                     # "cook 1 meat (beef / mutton / pork / chicken)", "breed 1 chick", 
                     # "make 1 bread and cook 1 meat (beef / mutton / pork / chicken)", "make 8 cookies"
                     ]
test_sub_goals = ["craft crafting table", "craft wooden pickaxe", "craft stone pickaxe", "craft iron pickaxe", "mine diamond"]
test_skills = ["collect flowers"]
farming_sub_goals = [["craft wooden hoe", "collect wheat seed", "hoe farm land", "plant 1 wheat seed", "kill pig", "craft furnace", "mine coal ore", "cook porkchop"],
                     ["craft wooden hoe", "collect melon", "collect melon seed", "collect pumpkin", "collect pumpkin seed", "hoe farm land", "plant 1 melon seed"],
                     ["craft a pair of shears", "shear one sheep", "craft bucket", "collect milk"],
                     ["craft wooden hoe", "collect wheat seed", "hoe farm land", "plant 1 wheat seed"], 
                     ["craft a pair of shears", "shear one sheep"],
                     ["craft bucket", "collect milk"],
                     ["collect wheat seed", "breed chicken"],
                     ["kill pig", "craft furnace", "mine coal ore", "cook porkchop"],
                     ["craft wooden hoe", "collect wheat seed", "hoe farm land", "plant 1 wheat seed", "plant 1 wheat seed", "collect wheat", "collect wheat", "breed sheep"],
                     ["craft wooden hoe", "collect melon", "collect melon seed", "hoe farm land", "plant 1 melon seed"],  
                     ["craft wooden hoe", "collect pumpkin", "collect pumpkin seed", "hoe farm land", "plant 1 pumpkin seed"]]
# voyager.learn()
# for farming_sub_goal in farming_sub_goals:
#     while True:
#         try:
#             voyager.inference_sub_goal(task="subgoal_farming", sub_goals=farming_sub_goal)
#             break
#         except Exception as e:
#             print("error:", e)
while True:
    voyager.inference_sub_goal(task="skill_test", sub_goals=test_skills)
while True:
    for goal in farming_task_list:
        while True:
            try:
                voyager.learn(goals = goal)
                break
            except Exception as e:
                print("error:", e)
for task in multi_mob_list:
    while True:
        try:
            voyager.inference(task=task)
            break
        except Exception as e:
            print("error:", e)
for task in many_mob_list:
    while True:
        try:
            voyager.inference(task=task)
            break
        except Exception as e:
            print("error:", e)