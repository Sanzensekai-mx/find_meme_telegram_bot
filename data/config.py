import os
from boto.s3.connection import S3Connection
# from dotenv import load_dotenv

# load_dotenv()
BOT_TOKEN = S3Connection(os.environ['BOT_TOKEN'])
# BOT_TOKEN = None
admins = S3Connection(os.environ['admins'])
# admins = []

# with open(os.path.join(os.getcwd(), 'data', 'secret_data.txt'), 'r') as f:
#     secret_data = []
#     for line in f:
#         secret_data.append(line.strip())
#     BOT_TOKEN = secret_data[0]
#     for elem in secret_data[1:]:
#         admins.append(elem)

# ip = os.getenv("ip")
