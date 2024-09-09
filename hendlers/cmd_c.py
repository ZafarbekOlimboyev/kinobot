from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import menu_admin, super_admin, follow_channel
from DATA_BASE.database import database_user, database_channel
from config import db_name
from functions.cheak import cheak_channels
from States.statess import RegistrState

cmd_co = Router()


@cmd_co.message(Command("start"))
async def cmd_start(msg: Message, state: FSMContext):
    db = database_user(db_name)
    db_channel = database_channel(db_name)
    channels = db_channel.all_channel()
    user = db.get_user(msg.from_user.id)
    if user is None:
        db.add_new_user(msg.from_user.id, msg.from_user.last_name, msg.from_user.first_name, msg.from_user.username)
        user = db.get_user(msg.from_user.id)
        # info = (f"Tarjima Kinolar bot\n"
        #         f"Botga yangi foydalanuvchi qo'shildi\n\n\tNikname : {msg.from_user.full_name}\n\tUsername: @{msg.from_user.username}\n\nBotdagi foydalanuvchilar soni: {user[0]}")
        # await msg.bot.send_message(chat_id=-1002105566390, text=info)
        if channels:
            cheak_answer = await cheak_channels(user_id=msg.from_user.id, bot=msg.bot)
            if cheak_answer:
                await msg.answer(text=f"Assalomu Alaykum {msg.from_user.full_name}!\n"
                                      "Botni to'liq ishlatish uchun kanallarga obuna bo'lishingiz kerak", reply_markup=follow_channel())
                await state.set_state(RegistrState.channel)

            else:
                await msg.answer(text=f"Assalomu Alaykum {msg.from_user.full_name}!\n\n\t✍🏻Kinoni kodini yuboring.")
                await state.clear()
        else:
            await msg.answer(text=f"Assalomu Alaykum {msg.from_user.full_name}!\n\n\t✍🏻Kinoni kodini yuboring.")
            await state.clear()
    elif user[4] == 1:
        await msg.answer(text=f'Assalomu Alaykum {user[2]}!', reply_markup=menu_admin)
        await state.clear()
    elif user[4] == 2:
        await msg.answer(text=f'Assalomu Alaykum {user[2]}!', reply_markup=super_admin)
        await state.clear()
    else:
        if channels:
            cheak_answer = await cheak_channels(user_id=msg.from_user.id, bot=msg.bot)
            if cheak_answer:
                await msg.answer(text="Siz kanallarga obuna bo'lmagansiz", reply_markup=follow_channel())
                await state.set_state(RegistrState.channel)
            else:
                await msg.answer(text=f"Assalomu Alaykum {msg.from_user.full_name}!\n\n\t✍🏻Kinoni kodini yuboring.")
                await state.clear()
        else:
            await msg.answer(text=f"Assalomu Alaykum {msg.from_user.full_name}!\n\n\t✍🏻Kinoni kodini yuboring.")
            await state.clear()


@cmd_co.callback_query(RegistrState.channel)
async def exapmle(msg: CallbackQuery, state: FSMContext):
    cheak_answer = await cheak_channels(user_id=msg.from_user.id, bot=msg.bot)
    if cheak_answer:
        await msg.answer(text="Siz kanallarga obuna bo'lmagansiz", reply_markup=follow_channel())
    else:
        await msg.bot.send_message(chat_id=msg.message.chat.id, text=f"Assalomu Alaykum {msg.from_user.full_name}!\n\n\t✍🏻Kinoni kodini yuboring.")
        await msg.bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message.message_id)
        await state.clear()

