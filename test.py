from voyager import Voyager

mc_port = 57996
env_wait_ticks = 100

voyager = Voyager(
    mc_port=mc_port,
    env_wait_ticks=env_wait_ticks,
    skill_library_dir="./skill_library"
)

# start lifelong learning
# voyager.learn()

# task = ""
# sub_goals = voyager.decompose_task(task=task)
sub_goals = ["craft diamond pickaxe"]
voyager.inference(sub_goals=sub_goals)