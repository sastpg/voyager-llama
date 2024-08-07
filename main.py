from odyssey import Odyssey
from odyssey.utils import config
from odyssey.utils.logger import get_logger
from odyssey.agents.llama import ModelType

import traceback
logger = get_logger('main')
mc_port = config.get('MC_SERVER_PORT')
mc_host = config.get('MC_SERVER_HOST')
node_port = config.get('NODE_SERVER_PORT')
embedding_dir = config.get('SENTENT_EMBEDDING_DIR')
# mc_host = "localhost"
# mc_port = 25576
# embedding_dir = '/home/jovyan/notebook/mc_voyager/sentent-embedding'
# embedding_dir = "D:\DESKTOP\paraphrase-multilingual-MiniLM-L12-v2" # local dir
# mc_host = "127.0.0.1"
# mc_port = 49741 # local server
env_wait_ticks = 100
def test_subgoal():
    voyager_l3_8b = Odyssey(
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
        critic_agent_model_name = ModelType.LLAMA3_8B_V3,
        comment_agent_model_name = ModelType.LLAMA3_8B_V3,
        planer_agent_qa_model_name = ModelType.LLAMA3_8B_V3,
        planer_agent_model_name = ModelType.LLAMA3_8B_V3,
        action_agent_model_name = ModelType.LLAMA3_8B_V3,
    )
    voyager_l3_70b = Odyssey(
        mc_port=mc_port,
        mc_host=mc_host,
        env_wait_ticks=env_wait_ticks,
        skill_library_dir="./skill_library",
        reload=False, # set to True if the skill_json updated
        embedding_dir=embedding_dir, # your model path
        # embedding_dir="/home/MCagent/paraphrase-multilingual-MiniLM-L12-v2", # linux model path
        environment='subgoal',
        resume=False,
        server_port=node_port,
        critic_agent_model_name = ModelType.LLAMA3_70B_V1,
        comment_agent_model_name = ModelType.LLAMA3_70B_V1,
        planer_agent_qa_model_name = ModelType.LLAMA3_70B_V1,
        planer_agent_model_name = ModelType.LLAMA3_70B_V1,
        action_agent_model_name = ModelType.LLAMA3_70B_V1,
    )
    # 5 classic MC tasks
    test_sub_goals = ["craft crafting table", "craft wooden pickaxe", "craft stone pickaxe", "craft iron pickaxe", "mine diamond"]
    while True:
        try:
            voyager_l3_8b.inference_sub_goal(task="subgoal_llama3_8b_v3", sub_goals=test_sub_goals)
            voyager_l3_70b.inference_sub_goal(task="subgoal_llama3_70b_v1", sub_goals=test_sub_goals)
        except Exception as e:
            logger.critical(e)
            traceback.print_exc()
def test_combat():
    voyager_l3_8b_v3 = Odyssey(
        mc_port=mc_port,
        mc_host=mc_host,
        env_wait_ticks=env_wait_ticks,
        skill_library_dir="./skill_library",
        reload=True, # set to True if the skill_json updated
        embedding_dir=embedding_dir, # your model path
        # embedding_dir="/home/MCagent/paraphrase-multilingual-MiniLM-L12-v2", # linux model path
        environment='combat',
        resume=False,
        server_port=node_port,
        critic_agent_model_name = ModelType.LLAMA3_8B_V3,
        comment_agent_model_name = ModelType.LLAMA3_8B_V3,
        planer_agent_qa_model_name = ModelType.LLAMA3_8B_V3,
        planer_agent_model_name = ModelType.LLAMA3_8B_V3,
        action_agent_model_name = ModelType.LLAMA3_8B_V3,
    )
    voyager_l3_8b = Odyssey(
        mc_port=mc_port,
        mc_host=mc_host,
        env_wait_ticks=env_wait_ticks,
        skill_library_dir="./skill_library",
        reload=True, # set to True if the skill_json updated
        embedding_dir=embedding_dir, # your model path
        # embedding_dir="/home/MCagent/paraphrase-multilingual-MiniLM-L12-v2", # linux model path
        environment='combat',
        resume=False,
        server_port=node_port,
        critic_agent_model_name = ModelType.LLAMA3_8B,
        comment_agent_model_name = ModelType.LLAMA3_8B,
        planer_agent_qa_model_name = ModelType.LLAMA3_8B,
        planer_agent_model_name = ModelType.LLAMA3_8B,
        action_agent_model_name = ModelType.LLAMA3_8B,
    )
    voyager_l3_70b = Odyssey(
        mc_port=mc_port,
        mc_host=mc_host,
        env_wait_ticks=env_wait_ticks,
        skill_library_dir="./skill_library",
        reload=True, # set to True if the skill_json updated
        embedding_dir=embedding_dir, # your model path
        # embedding_dir="/home/MCagent/paraphrase-multilingual-MiniLM-L12-v2", # linux model path
        environment='combat',
        resume=False,
        server_port=node_port,
        critic_agent_model_name = ModelType.LLAMA3_70B_V1,
        comment_agent_model_name = ModelType.LLAMA3_70B_V1,
        planer_agent_qa_model_name = ModelType.LLAMA3_70B_V1,
        planer_agent_model_name = ModelType.LLAMA3_70B_V1,
        action_agent_model_name = ModelType.LLAMA3_70B_V1,
    )
    
    multi_rounds_tasks = ["1 zombie", "3 zombie"]
    MAX_RETRY  = 3
    while True:
        # for task in combat_benchmark:
        retry = MAX_RETRY  
        i = 0
        while i < len(multi_rounds_tasks):
            try:
                voyager_l3_8b_v3.inference(task=multi_rounds_tasks[i], reset_env=False, feedback_rounds=3)
                i += 1
                retry = MAX_RETRY
            except Exception as e:
                logger.critical(multi_rounds_tasks[i]+' failed. retry...')
                logger.critical(e)
                traceback.print_exc()
                if retry > 0:
                    retry -= 1
                    continue
                i += 1
                retry = MAX_RETRY

def explore():
    voyager_l3_8b = Odyssey(
        mc_port=mc_port,
        mc_host=mc_host,
        env_wait_ticks=env_wait_ticks,
        skill_library_dir="./skill_library",
        reload=True, # set to True if the skill_json updated
        embedding_dir=embedding_dir, # your model path
        # embedding_dir="/home/MCagent/paraphrase-multilingual-MiniLM-L12-v2", # linux model path
        environment='explore',
        resume=False,
        server_port=node_port,
        critic_agent_model_name = ModelType.LLAMA3_8B,
        comment_agent_model_name = ModelType.LLAMA3_8B,
        planer_agent_qa_model_name = ModelType.LLAMA3_8B,
        planer_agent_model_name = ModelType.LLAMA3_8B,
        action_agent_model_name = ModelType.LLAMA3_8B,
        # because I wrongly added username bot1_13b in minecraft, so use this name
        # rather then bot1_8b
        username='bot1_13b'
    )
    voyager_l3_8b_v3 = Odyssey(
        mc_port=mc_port,
        mc_host=mc_host,
        env_wait_ticks=env_wait_ticks,
        skill_library_dir="./skill_library",
        reload=True, # set to True if the skill_json updated
        embedding_dir=embedding_dir, # your model path
        # embedding_dir="/home/MCagent/paraphrase-multilingual-MiniLM-L12-v2", # linux model path
        environment='explore',
        resume=False,
        server_port=node_port,
        critic_agent_model_name = ModelType.LLAMA3_8B_V3,
        comment_agent_model_name = ModelType.LLAMA3_8B_V3,
        planer_agent_qa_model_name = ModelType.LLAMA3_8B_V3,
        planer_agent_model_name = ModelType.LLAMA3_8B_V3,
        action_agent_model_name = ModelType.LLAMA3_8B_V3,
        username='bot1_13b_v3'
    )
    voyager_l3_70b = Odyssey(
        mc_port=mc_port,
        mc_host=mc_host,
        env_wait_ticks=env_wait_ticks,
        skill_library_dir="./skill_library",
        reload=True, # set to True if the skill_json updated
        embedding_dir=embedding_dir, # your model path
        # embedding_dir="/home/MCagent/paraphrase-multilingual-MiniLM-L12-v2", # linux model path
        environment='explore',
        resume=False,
        server_port=node_port,
        critic_agent_model_name = ModelType.LLAMA3_70B_V1,
        comment_agent_model_name = ModelType.LLAMA3_70B_V1,
        planer_agent_qa_model_name = ModelType.LLAMA3_70B_V1,
        planer_agent_model_name = ModelType.LLAMA3_70B_V1,
        action_agent_model_name = ModelType.LLAMA3_70B_V1,
        username='bot1_70b_v1'
    )
    voyager_l3_8b_v3.learn()
    voyager_l3_8b.learn()
    voyager_l3_70b.learn()

def test_farming():
    voyager_l3_8b = Odyssey(
        mc_port=mc_port,
        mc_host=mc_host,
        env_wait_ticks=env_wait_ticks,
        skill_library_dir="./skill_library",
        reload=True, # set to True if the skill_json updated
        embedding_dir=embedding_dir, # your model path
        # embedding_dir="/home/MCagent/paraphrase-multilingual-MiniLM-L12-v2", # linux model path
        environment='farming',
        resume=False,
        server_port=node_port,
        critic_agent_model_name = ModelType.LLAMA3_8B_V3,
        comment_agent_model_name = ModelType.LLAMA3_8B_V3,
        planer_agent_qa_model_name = ModelType.LLAMA3_8B_V3,
        planer_agent_model_name = ModelType.LLAMA3_8B_V3,
        action_agent_model_name = ModelType.LLAMA3_8B_V3,
    )
    voyager_l3_70b = Odyssey(
        mc_port=mc_port,
        mc_host=mc_host,
        env_wait_ticks=env_wait_ticks,
        skill_library_dir="./skill_library",
        reload=True, # set to True if the skill_json updated
        embedding_dir=embedding_dir, # your model path
        # embedding_dir="/home/MCagent/paraphrase-multilingual-MiniLM-L12-v2", # linux model path
        environment='farming',
        resume=False,
        server_port=node_port,
        critic_agent_model_name = ModelType.LLAMA3_70B_V1,
        comment_agent_model_name = ModelType.LLAMA3_70B_V1,
        planer_agent_qa_model_name = ModelType.LLAMA3_70B_V1,
        planer_agent_model_name = ModelType.LLAMA3_70B_V1,
        action_agent_model_name = ModelType.LLAMA3_70B_V1,
    )
    farming_benchmark = [
                    "collect 1 seed (wheat or melon or pumpkin)"
                    ]
    while True:
        # for task in farming_benchmark:
        i = 0
        while i < len(farming_benchmark):
            try:
                voyager_l3_70b.learn(goals=farming_benchmark[i], reset_env=False)
                i += 1
            except Exception as e:
                logger.critical(farming_benchmark[i]+' failed. retry...')
                logger.critical(e)
                traceback.print_exc() 
        i = 0
        while i < len(farming_benchmark):
            try:
                voyager_l3_8b.learn(goals=farming_benchmark[i], reset_env=False)
                i += 1
            except Exception as e:
                logger.critical(farming_benchmark[i]+' failed. retry...')
                logger.critical(e)
                traceback.print_exc()

if __name__ == '__main__':
    test_farming()