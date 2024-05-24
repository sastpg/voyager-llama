from voyager import Voyager
from voyager.utils import config
mc_port = config.get('MC_SERVER_PORT')
mc_host = config.get('MC_SERVER_HOST')
embedding_dir = config.get('SENTENT_EMBEDDING_DIR')

mc_host = "10.214.211.110"
mc_port = 25565
# mc_host = "127.0.0.1"
# mc_port = 49741 # local server
embedding_dir = "D:\DESKTOP\paraphrase-multilingual-MiniLM-L12-v2" # local dir
env_wait_ticks = 100

voyager = Voyager(
    mc_port=mc_port,
    mc_host=mc_host,
    env_wait_ticks=env_wait_ticks,
    skill_library_dir="./skill_library",
    reload=True, # set to True if the skill_json updated
    embedding_dir=embedding_dir, # your model path
    environment='combat'
)
combat_benchmark = [
                    # Single-mob tasks
                    "1 zombie", "1 skeleton",  "1 spider", "1 zombified_piglin", "1 enderman",
                    # Multi-mob tasks
                    "3 zombie", "5 zombie", "1 zombie, 1 skeleton", "1 zombie, 1 spider", "1 zombie, 1 skeleton, 1 spider"
                    ]
farming_benchmark = [
                    # Single-goal tasks
                    "hoe a farmland", "breed 1 chicken", "collect 1 wool by shears or collect 1 bucket of milk",
                    "cook meat (beef / mutton / pork / chicken)", "plant 1 seed (wheat / melon / pumpkin)",
                    # Multi-goal tasks
                    "plant 1 seed (wheat / melon / pumpkin) and cook 1 meat (beef / mutton / pork / chicken)",
                    "collect 1 wheat and cook 1 meat  (beef / mutton / pork / chicken)",
                    "collect 1 wool by shears and collect 1 bucket of milk",
                    "breed 1 sheep and collect 1 wool by shears",
                    "make cookies"
                    ]
# 5 classic MC tasks
test_sub_goals = ["craft crafting table", "craft wooden pickaxe", "craft stone pickaxe", "craft iron pickaxe", "mine diamond"]
# skill test
test_skills = ["collect flowers"]
# voyager.learn()
while True:
    voyager.inference_sub_goal(task="subgoal_test", sub_goals=test_skills)
while True:
    for goal in farming_benchmark:
        while True:
            try:
                voyager.learn(goals = goal)
                break
            except Exception as e:
                print("error:", e)
for task in combat_benchmark:
    while True:
        try:
            voyager.inference(task=task)
            break
        except Exception as e:
            print("error:", e)