import os
import json
from pathlib import Path
CONFIG_FILE_PATH = Path(__file__).parent.parent.parent / 'conf/config.json'
class ConfigManager:
    def __init__(self):
        with open(CONFIG_FILE_PATH, 'r') as f:
            self.config = json.load(f)
        self.config = self.config | {
            'MC_SERVER_HOST': os.getenv('MC_SERVER_HOST', 'localhost'),
            'MC_SERVER_PORT': os.getenv('MC_SERVER_PORT', '25565'),
            'SENTENT_EMBEDDING_DIR': os.getenv('SENTENT_EMBEDDING_DIR', '/sentent-embedding')
        }
    def get(self, key:str)->str:
        return self.config.get(key, '')