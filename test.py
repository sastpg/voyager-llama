from voyager import Voyager

mc_port = 64639
env_wait_ticks = 100

voyager = Voyager(
    mc_port=mc_port,
    env_wait_ticks=env_wait_ticks,
    skill_library_dir="./skill_library",
    reload=False, # set to True if the skill_json updated
    embedding_dir="d:\\DESKTOP\\paraphrase-multilingual-MiniLM-L12-v2", # your model path
    environment='combat'
)

task = "5 skeleton"

# sub_goals = voyager.decompose_task(task = '')
# print(sub_goals)
# test_sub_goals = ["craft wooden sword"]
# voyager.learn()
voyager.inference(task = task)
