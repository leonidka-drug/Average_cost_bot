from environs import Env

env = Env()
env.read_env()

CREDENTIALS_FILE = "data/creds.json"
BOT_TOKEN = env.str("BOT_TOKEN")
ADMIN = env.str("ADMIN")
spreadsheet_id = env.str("spreadsheet_id")
