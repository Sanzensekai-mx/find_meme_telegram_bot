import json
import asyncio
from utils.db_api.models import DBCommands
from utils.db_api.database import db as gino
from gino import Gino
from gino.schema import GinoSchemaVisitor
from data.config import POSTGRES_URI

# gino = Gino()
db = DBCommands()

loop = asyncio.get_event_loop()


async def add(meme, value):
    await db.add_meme(
        meme_name=meme,
        meme_describe=value['describe'],
        meme_href=value['meme_href'],
        meme_photo_href=value['pic_href'])


# Запускать после запуска app.py
async def main():
    async with gino.with_bind(POSTGRES_URI):
        with open('mem_dataset.json', 'r', encoding='utf-8') as meme_data:
            memes = json.load(meme_data)
            for meme, value in memes.items():
                await add(meme, value)
            print('Заполнение БД завершено.')


loop.run_until_complete(main())
