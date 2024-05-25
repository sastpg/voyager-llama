
from voyager import Voyager
from voyager.utils import config
from voyager.agents.llama import ModelType
mc_port = config.get('MC_SERVER_PORT')
mc_host = config.get('MC_SERVER_HOST')
node_port = config.get('NODE_SERVER_PORT')
embedding_dir = config.get('SENTENT_EMBEDDING_DIR')
mc_host = "localhost"
mc_port = 25576
embedding_dir = '/home/jovyan/notebook/mc_voyager/sentent-embedding'

mc_host = "10.214.211.110"
mc_port = 25565
embedding_dir = "D:\DESKTOP\paraphrase-multilingual-MiniLM-L12-v2" # local dir

env_wait_ticks = 100
def test_subgoal():
    voyager = Voyager(
        mc_port=mc_port,
        mc_host=mc_host,
        env_wait_ticks=env_wait_ticks,
        skill_library_dir="./skill_library",
        reload=True, # set to True if the skill_json updated
        embedding_dir=embedding_dir, # your model path
        # embedding_dir="/home/MCagent/paraphrase-multilingual-MiniLM-L12-v2", # linux model path
        environment='subgoal',
        resume=False,
        server_port=node_port,
        critic_agent_model_name = ModelType.LLAMA2_70B,
        comment_agent_model_name = ModelType.LLAMA2_70B,
        curriculum_agent_qa_model_name = ModelType.LLAMA2_70B,
        curriculum_agent_model_name = ModelType.LLAMA2_70B,
        action_agent_model_name = ModelType.LLAMA2_70B,
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
        reload=True, # set to True if the skill_json updated
        embedding_dir=embedding_dir, # your model path
        # embedding_dir="/home/MCagent/paraphrase-multilingual-MiniLM-L12-v2", # linux model path
        environment='combat',
        resume=False,
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
    test_combat()