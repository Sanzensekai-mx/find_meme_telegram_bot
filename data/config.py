import os
from dotenv import load_dotenv

load_dotenv()
# BOT_TOKEN = str(os.environ.get('BOT_TOKEN'))
# BOT_TOKEN = None
# admins = str(os.environ.get('admins')).split(', ')
# admins = []
#
# with open(os.path.join(os.getcwd(), 'data', 'secret_data.txt'), 'r') as f:
#     secret_data = []
#     for line in f:
#         secret_data.append(line.strip())
#     BOT_TOKEN = secret_data[0]
#     for elem in secret_data[1:]:
#         admins.append(elem)

BOT_TOKEN = os.getenv("BOT_TOKEN")
admins = str(os.getenv("admins")).split(', ')

host = os.getenv("PG_HOST")
PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")
DATABASE = str(os.getenv("DATABASE"))

ip = os.getenv("ip")

# Ссылка подключения к базе данных
POSTGRES_URI = f"postgresql://{PG_USER}:{PG_PASS}@{ip}/{DATABASE}"
