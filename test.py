from voyager import Voyager

mc_port = 49153
# mc_port = 25565 # linux server port
env_wait_ticks = 100

voyager = Voyager(
    mc_port=mc_port,
    env_wait_ticks=env_wait_ticks,
    skill_library_dir="./skill_library",
    reload=True, # set to True if the skill_json updated
    embedding_dir="d:\\DESKTOP\\paraphrase-multilingual-MiniLM-L12-v2", # your model path
    # embedding_dir="/home/MCagent/paraphrase-multilingual-MiniLM-L12-v2", # linux model path
    environment='combat'
)
single_mob_list = ["10 zombie", "1 skeleton", "1 spider", "1 cave_spider", "1 enderman", 
                   "1 blaze", "1 ghast", "1 piglin", "1 piglin_brute", "1 wither_skeleton"]
many_mob_list = ["3 zombie", "5 zombie", 
                 "3 skeleton", "5 skeleton"]
multi_mob_list = ["1 zombie, 1 skeleton, 1 spider",
                  "1 zombie, 1 enderman, 1 piglin_brute",
                  "2 zombie, 2 skeleton, 2 spider"]
farming_task_list = ["plant 1 wheat seed", "plant 1 melon seed or pumpkin seed", "collect 1 wool by shears or collect 1 bucket of milk", 
                     "cook 1 meat (beef / mutton / pork / chicken)", "breed 1 chick", 
                     "make 1 bread and cook 1 meat (beef / mutton / pork / chicken)", "make 8 cookies"]
test_sub_goals = ["craft crafting table", "craft wooden pickaxe", "craft stone pickaxe", "craft iron pickaxe", "mine diamond"]
# while True:
#     voyager.inference_sub_goal(task="subgoal_test", sub_goals=test_sub_goals)
for task in single_mob_list:
    voyager.inference(task=task)
# voyager.learn()