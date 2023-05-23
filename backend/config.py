import os
from dotenv import load_dotenv

def openai_key() -> str:
    return os.getenv('OPENAI_API_KEY')

def mongodb_conn_str() -> str:
    return os.getenv('MONGODB_CONN_STR')

def load_env() -> bool:
    cfg_file = os.path.join(os.path.expanduser('~'), '.mykbs')
    print(f'Loading env from {cfg_file}')
    if os.path.exists(cfg_file):
        load_dotenv(cfg_file) 
        return True
    else:
        return False


