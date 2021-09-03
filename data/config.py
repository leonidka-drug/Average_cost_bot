from environs import Env

env = Env()
env.read_env()

CREDENTIALS_FILE = "creds.json"
BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
spreadsheet_id = env.str("spreadsheet_id")
