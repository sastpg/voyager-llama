from voyager import Voyager

mc_port = 55351
env_wait_ticks = 100

voyager = Voyager(
    mc_port=mc_port,
    env_wait_ticks=env_wait_ticks,
    skill_library_dir="./skill_library",
    reload=False, # set to True if the skill_json updated
    embedding_dir="d:\\DESKTOP\\paraphrase-multilingual-MiniLM-L12-v2", # your model path
    environment='combat'
)
task_z = "1 zombie"
single_mob_list = ["1 zombie", "1 skeleton", "1 spider", "1 cave_spider", "1 enderman", 
                   "1 blaze", "1 ghast", "1 piglin", "1 piglin_brute", "1 wither_skeleton"]
# sub_goals = voyager.decompose_task(task = '')
# print(sub_goals)
# test_sub_goals = ["craft wooden sword"]
# voyager.learn()
for task in single_mob_list:
    voyager.inference(task=task)
