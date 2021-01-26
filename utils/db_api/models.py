from utils.db_api.database import db
from aiogram import types, Bot


class User(db.Model):
    __tablename__ = 'users'
    # Идентификатор чата с пользователем
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger)
    # Никнейм пользователя
    username = db.Column(db.String)
    full_name = db.Column(db.String)

    def __repr__(self):
        return "<User(id='{}', fullname='{}', username='{}')>".format(
            self.chat_id, self.full_name, self.username)


class Meme(db.Model):
    __tablename__ = 'meme_datatable'
    pic_href = db.Column(db.String)
    describe = db.Column(db.String)
    meme_href = db.Column(db.String)
    meme_name = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return "<Meme(id='{}', name='{}')>".format(
            self.id, self.meme_name)


class DBCommands:
    async def get_user(self, user_id):
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    async def add_new_user(self):
        user = types.User.get_current()
        old_user = await self.get_user(user.id)
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

    async def show_meme(self):
        items = await Meme.query.gino.all()
        return items