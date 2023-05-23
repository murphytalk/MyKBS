from config import load_env
from storage import Storage

if __name__ == "__main__":
    load_env()
    s = Storage()
    from bot.line_bot import run
    run(lambda msg : s.save_payload('line_messages', msg))
