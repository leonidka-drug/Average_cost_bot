from environs import Env
from pathlib import Path
from utils.db_api.sqlite import Database

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_FILE = BASE_DIR / "data/creds.json"
DATA_BASE_FILE = BASE_DIR / "data/db.db"
BOT_TOKEN = env.str("BOT_TOKEN")
ADMIN = env.str("ADMIN")
spreadsheet_id = env.str("spreadsheet_id")
db = Database(DATA_BASE_FILE)