import os

class EnvManager:
    def __init__(self):
        self.config = {
            'MC_SERVER_HOST': os.getenv('MC_SERVER_HOST', 'localhost'),
            'MC_SERVER_PORT': os.getenv('MC_SERVER_PORT', '25565'),
            'SENTENT_EMBEDDING_DIR': os.getenv('SENTENT_EMBEDDING_DIR', '/sentent-embedding')
        }