from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaVideo
from DATA_BASE.database import database_movie, database_user
from States.statess import RegistrState
from functions.send_kino import get_id
from keyboards.keyboards import follow_channel
from functions.cheak import cheak_channels

msg_co = Router()


@msg_co.message()
async def unknown_command(msg: Message):
    if await cheak_channels(msg.from_user.id, msg.bot):
        await msg.answer("Iltimos kanallarga obuna bo'ling", reply_markup=follow_channel())
    else:
        if msg.text.isdigit():
            file_id = get_id(int(msg.text))
            if file_id:
                await msg.bot.send_video(chat_id=msg.chat.id, video=file_id[1], caption=file_id[3])
            else:
                await msg.answer(text="Bunday kodli kino topilmadi.")
        else:
            await msg.answer(text="Iltimos faqat codni kiriting faqat raqamlardan iborat bo'lsin!")
