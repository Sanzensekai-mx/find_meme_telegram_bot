import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = str(os.environ.get('BOT_TOKEN'))
admins = str(os.environ.get('admins')).split(', ')
# ip = os.getenv("ip")
# BOT_TOKEN = os.getenv("BOT_TOKEN")
# admins = str(os.getenv("admins")).split(', ')
# host = os.getenv("PG_HOST")
# PG_USER = os.getenv("PG_USER")
# PG_PASS = os.getenv("PG_PASS")
