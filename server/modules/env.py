from dotenv import load_dotenv

def load_env():
    load_dotenv('.env.local')
    load_dotenv('.env')