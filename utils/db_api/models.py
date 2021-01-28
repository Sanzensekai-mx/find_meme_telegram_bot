from utils.db_api.database import db
from aiogram import types, Bot


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    full_name = db.Column(db.String)
    # Идентификатор чата с пользователем
    user_id = db.Column(db.BigInteger, unique=True)
    # Никнейм пользователя
    username = db.Column(db.String)

    def __repr__(self):
        return "<User(id='{}', fullname='{}', username='{}')>".format(
            self.chat_id, self.full_name, self.username)


class Meme(db.Model):
    __tablename__ = 'meme_datatable'
    id = db.Column(db.Integer, db.Sequence('meme_id_seq'), primary_key=True)
    meme_name = db.Column(db.String, unique=True)
    describe = db.Column(db.String)
    pic_href = db.Column(db.String)
    meme_href = db.Column(db.String)

    def __repr__(self):
        return "<Meme(id='{}', name='{}')>".format(
            self.id, self.meme_name)


class DBCommands:
    # Функция возвращает объект из таблицы User, если такой user_id существует в БД. Возвращает None, если такого нет
    async def get_user(self, user_id):
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    async def add_new_user(self):
        user = types.User.get_current()
        old_user = await self.get_user(user.id)  # get_user берет в качестве аргумента аттрибут id
        # типа telegram api User
        if old_user:
            return old_user
        new_user = User()
        new_user.user_id = user.id
        new_user.username = user.username
        new_user.full_name = user.full_name
        await new_user.create()
        return new_user

    async def count_users(self) -> int:
        total = await db.func.count(User.id).gino.scalar()
        return total

    async def get_meme(self, meme_name):
        meme = await Meme.query.where(Meme.meme_name == meme_name).gino.first()
        return meme

    async def is_this_meme_in_db(self, meme_name):
        meme = await self.get_meme(meme_name)
        if meme:
            return True
        else:
            return False

    async def show_meme(self):
        items = await Meme.query.gino.all()
        return items

    async def add_meme(self, meme_name, meme_describe=None, meme_href=None, meme_photo_href=None):
        old_meme = await self.get_meme(meme_name)
        # Обновляет мем, если такой уже существует в БД
        if old_meme:
            await old_meme.update(
                id=old_meme.id,
                meme_name=meme_name,
                meme_href=meme_href,
                describe=meme_describe,
                pic_href=meme_photo_href
            ).apply()
            return old_meme
        # Создание нового мема в БД
        new_meme = Meme()
        new_meme.meme_name = meme_name
        new_meme.meme_href = meme_href
        new_meme.describe = meme_describe
        new_meme.pic_href = meme_photo_href
        await new_meme.create()
        return new_meme

    async def del_meme(self, meme_name):
        meme = await self.get_meme(meme_name)
        if meme:
            await meme.delete()
            return meme
        return meme
