from config import load_env

if __name__ == "__main__":
    load_env()
    from bot.line_bot import run
    run()
