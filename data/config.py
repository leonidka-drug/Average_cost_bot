from environs import Env

env = Env()
env.read_env()

CREDENTIALS_FILE = "data/creds.json"
DATA_BASE_FILE = "data/db.db"
BOT_TOKEN = env.str("BOT_TOKEN")
ADMIN = env.str("ADMIN")
spreadsheet_id = env.str("spreadsheet_id")
