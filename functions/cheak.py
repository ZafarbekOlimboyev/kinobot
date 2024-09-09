from aiogram.types import Message

from config import db_name
from aiogram import Bot
from DATA_BASE.database import database_channel

async def CheakSub(user_id,bot,channel_id):
    try:
        user = await bot.get_chat_member(channel_id, user_id)
        if user.status in ["member","administrator","creator"]:
            return False
        return True
    except Exception as e:
        print(f"Error in cheak_sub: {e}")
        return True

async def cheak_channels(user_id,bot=Bot):
    db = database_channel(db_name)
    channels = db.all_channel()
    for i in channels:
        cheak = await CheakSub(user_id=user_id,bot=bot,channel_id=i[0])
        if cheak is False:
            continue
        else:
            return True
    return False