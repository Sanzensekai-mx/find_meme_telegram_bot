import os

BOT_TOKEN = str(os.environ.get('BOT_TOKEN'))

admins = str(os.environ.get('admins')).split(', ')
