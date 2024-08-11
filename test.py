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
env_wait_ticks = 100

def test_farming():
    odyssey_l3_70b = Odyssey(
        mc_port=mc_port,
        mc_host=mc_host,
        env_wait_ticks=env_wait_ticks,
        skill_library_dir="./skill_library",
        reload=True, # set to True if the skill_json updated
        embedding_dir=embedding_dir, # your model path
        environment='farming',
        resume=False,
        server_port=node_port,
        critic_agent_model_name = ModelType.LLAMA3_8B_V3,
        comment_agent_model_name = ModelType.LLAMA3_8B_V3,
        planner_agent_qa_model_name = ModelType.LLAMA3_8B_V3,
        planner_agent_model_name = ModelType.LLAMA3_8B_V3,
        action_agent_model_name = ModelType.LLAMA3_8B_V3,
    )
    farming_benchmark = [
                # "make 1 sugar",
                # "smelt 5 dye",
                "collect 1 bucket of water",
                "obtain 1 leather",
                "collect 1 bucket of water",
                ]
    i = 0
    while i <= 3:
        try:
            odyssey_l3_70b.learn(goals=farming_benchmark[i], reset_env=False)
            i += 1
        except Exception as e:
            logger.critical(farming_benchmark[i] +" failed. retry...")
            logger.critical(e)
            traceback.print_exc() 

def test_skill(skill_name):
    odyssey_skill = Odyssey(
        mc_port=mc_port,
        mc_host=mc_host,
        env_wait_ticks=env_wait_ticks,
        reload=True, # set to True if the skill_json updated
        embedding_dir=embedding_dir, # your model path
        resume=False,
        server_port=node_port,
    )
    odyssey_skill.run_raw_skill(f"./skill_library/skill/compositional/{skill_name}", reset=True)
    while True:
        odyssey_skill.run_raw_skill(f"./skill_library/skill/compositional/{skill_name}", reset=False)

if __name__ == '__main__':
    test_farming()