from voyager import Voyager

mc_port = 57996
env_wait_ticks = 100

voyager = Voyager(
    mc_port=mc_port,
    env_wait_ticks=env_wait_ticks,
    openai_api_key="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",
    skill_library_dir="./skill_library"
)

# start lifelong learning
# voyager.learn()

# task = ""
# sub_goals = voyager.decompose_task(task=task)
sub_goals = ["craft diamond pickaxe"]
voyager.inference(sub_goals=sub_goals)