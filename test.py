from voyager import Voyager

mc_port = 50806
env_wait_ticks = 100

voyager = Voyager(
    mc_port=mc_port,
    env_wait_ticks=env_wait_ticks,
    skill_library_dir="./skill_library",
    reload=False, # set to True if the skill_json updated
    embedding_dir="d:\\DESKTOP\\paraphrase-multilingual-MiniLM-L12-v2", # your model path
    # embedding_dir="/home/MCagent/paraphrase-multilingual-MiniLM-L12-v2", # linux model path
    environment='combat'
)
task_z = "1 zombie"
single_mob_list = ["1 zombie", "1 skeleton", "1 spider", "1 cave_spider", "1 enderman", 
                   "1 blaze", "1 ghast", "1 piglin", "1 piglin_brute", "1 wither_skeleton"]
test_sub_goals = [["craft crafting table"], ["craft wooden pickaxe"], ["craft stone pickaxe"], ["craft iron pickaxe"], ["mine diamond"]]
for test_sub_goal in test_sub_goals:
    voyager.inference_sub_goal(task="subgoal_test", sub_goals=test_sub_goal)
    voyager.respawn_and_clear()
for task in single_mob_list:
    voyager.inference(task=task)
# voyager.learn()