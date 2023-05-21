import os
from dotenv import dotenv_values

env:dict = {}
env_loaded = False

def openai_key() -> str:
    return env['OPENAI_API_KEY']

def mongodb_conn_str() -> str:
    return env['MONGODB_CONN_STR']

def load_env() -> bool:
    global env, env_loaded
    cfg_file = os.path.join(os.path.expanduser('~'), '.mykbs')
    print(f'Loading env from {cfg_file}')
    if os.path.exists(cfg_file):
        env = dotenv_values(cfg_file) 
        env_loaded = True
        return True
    else:
        return False


