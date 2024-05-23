
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
def test_subgoal():
    voyager = Voyager(
        mc_port=mc_port,
        mc_host=mc_host,
        env_wait_ticks=env_wait_ticks,
        skill_library_dir="./skill_library",
        reload=False, # set to True if the skill_json updated
        embedding_dir=embedding_dir, # your model path
        # embedding_dir="/home/MCagent/paraphrase-multilingual-MiniLM-L12-v2", # linux model path
        environment='subgoal',
        resume=True,
    )
    # 5 classic MC tasks
    test_sub_goals = ["craft crafting table", "craft wooden pickaxe", "craft stone pickaxe", "craft iron pickaxe", "mine diamond"]
    while True:
        voyager.inference_sub_goal(task="subgoal_test", sub_goals=test_sub_goals)
def test_combat():
    voyager = Voyager(
        mc_port=mc_port,
        mc_host=mc_host,
        env_wait_ticks=env_wait_ticks,
        skill_library_dir="./skill_library",
        reload=False, # set to True if the skill_json updated
        embedding_dir=embedding_dir, # your model path
        # embedding_dir="/home/MCagent/paraphrase-multilingual-MiniLM-L12-v2", # linux model path
        environment='combat',
        resume=True,
    )
    combat_benchmark = [
                        # Single-mob tasks
                        "1 zombie", "1 skeleton",  "1 spider", "1 zombified_piglin", "1 enderman",
                        # Multi-mob tasks
                        "3 zombie", "5 zombie", "1 zombie, 1 skeleton", "1 zombie, 1 spider", "1 zombie, 1 skeleton, 1 spider"
                        ]
    while True:
        for task in combat_benchmark:
            voyager.inference(task=task)

if __name__ == '__main__':
    test_subgoal()