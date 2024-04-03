from voyager import Voyager

mc_port = 54185
env_wait_ticks = 100

voyager = Voyager(
    mc_port=mc_port,
    env_wait_ticks=env_wait_ticks,
    skill_library_dir="./skill_library",
    reload=True, # set to True if the skill_json updated
    embedding_dir="d:\\DESKTOP\\paraphrase-multilingual-MiniLM-L12-v2" # your model path
)

# start lifelong learning
# voyager.learn()

# task = ""
# sub_goals = voyager.decompose_task(task=task)
combat_sub_goals = ["craft iron sword", "craft iron helmet", "craft iron chestplate", "craft iron leggings", "craft iron boots", "equip sword", "equip iron armor"]
sheep_sub_goals = ["craft shears", "shear one sheep"]
voyager.inference(sub_goals=sheep_sub_goals)