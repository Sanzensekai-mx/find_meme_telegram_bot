import os

from dotenv import load_dotenv

load_dotenv()

# BOT_TOKEN = str(os.getenv())
BOT_TOKEN = None
# admins = [os.getenv(),]
admins = []

with open(os.path.join(os.getcwd(), 'data', 'secret_data.txt'), 'r') as f:
    secret_data = []
    for line in f:
        secret_data.append(line.strip())
    BOT_TOKEN = secret_data[0]
    for elem in secret_data[1:]:
        admins.append(elem)

ip = os.getenv("ip")
