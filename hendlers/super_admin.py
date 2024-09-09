from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from DATA_BASE import database
from States.admin_state import AdminState
from config import db_name
from keyboards.keyboards import (
    channel_list_k, menu, yes_or_noo,
    bekor_qilish, super_admin,
    yes_or_no_admin, menu_admin,
    admin_list_k
)

super_admin_r = Router()
#---------------------------Super admin panel functions--------------------------------------------------------------------------------------#


#---------------------------"Yangi admin qo'shish" funksiyasi---------------------------------------------------------------------------------#

#___________________________________________START_____________________________________________________________________________________________#


@super_admin_r.message(F.text == "Yangi admin qo'shish")
async def new_admin(msg: Message, state: FSMContext):
    dbm = database.database_user(db_name)
    user = dbm.get_user(msg.from_user.id)
    if user[4] == 2:
        await msg.answer(text="Yangi adminni telegram idsini yuboring yoki"
                              " yangi admin qilmoqchi bo'lgan userdan botga xabar uzating(froward qiling)",
                         reply_markup=bekor_qilish)
        await state.set_state(AdminState.new_admin)
    else:
        await msg.answer(text="Buday menyu yo'q")


#---------------------------------------------------------------------------------------------------------------------------------------------#

@super_admin_r.message(AdminState.new_admin)
async def admin(msg: Message, state: FSMContext):
    if msg.text == "Bekor qilish":
        await msg.answer(text="Bekor qilindi.", reply_markup=super_admin)
        await state.clear()
    else:
        dmb = database.database_user(db_name)
        try:
            user = dmb.get_user(msg.forward_from.id)
            if user:
                info = f"Foydalanuvchi haqida ma'lumot\n\n\tIsm : {msg.forward_from.first_name}\n\tTelegram id : {msg.forward_from.id}\n\tUsername : @{msg.forward_from.username}\nAdminlikka tayinlansinmi ?"
                await msg.answer(text=info, reply_markup=yes_or_no_admin)
                await state.update_data(tg_id=user[1])
            else:
                await msg.answer(text="Bunday telegram idli foydalanuvchi topilmadi.\nQayta kiritib ko'ring.",
                                 reply_markup=bekor_qilish)
        except:
            if msg.text.isdigit():
                user = dmb.get_user(int(msg.text))
                if user:
                    info = f"Foydalanuvchi haqida ma'lumot\n\n\tIsm : {user[2]}\n\tTelegram id : {user[1]}\n\tUsername : @{user[5]}\nAdminlikka tayinlansinmi ?"
                    await msg.answer(text=info, reply_markup=yes_or_no_admin)
                    await state.update_data(tg_id=user[1])
                else:
                    await msg.answer(text="Bunday telegram idli foydalanuvchi topilmadi.\nQayta kiritib ko'ring.",
                                     reply_markup=bekor_qilish)
            else:
                await msg.answer(text="Telegram id faqat raqamlardan iborat bo'ladi yoki "
                                      "agar siz habarni uzatgan bo'sangiz bu foydalanuvchini ma'lumotlarini"
                                      " olishda muammo yuzaga keldi. \nQayta kiritib ko'ring.",
                                 reply_markup=bekor_qilish)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

@super_admin_r.callback_query(AdminState.new_admin)
async def admin(query: CallbackQuery, state: FSMContext):
    dbm = database.database_user(db_name)
    data = await state.get_data()
    tg_id = data.get("tg_id")
    if query.data == "admin":
        dbm.update_admin(tg_id=tg_id,new_admin_id=1)
        await query.answer("Yangi admin qo'shildi")
        await query.bot.delete_message(chat_id=query.from_user.id,message_id=query.message.message_id)
        await query.bot.send_message(chat_id=tg_id,text="Tabriklaymiz. Siz adminlikka tayinlandingiz.",reply_markup=menu_admin)
        await query.message.answer(text="Menyu",reply_markup=super_admin)
    elif query.data == "super":
        dbm.update_admin(tg_id=tg_id,new_admin_id=2)
        await query.answer("Yangi Super admin qo'shildi")
        await query.bot.delete_message(chat_id=query.from_user.id,message_id=query.message.message_id)
        await query.bot.send_message(chat_id=tg_id,text="Tabriklaymiz. Siz Super adminlikka tayinlandingiz.",reply_markup=super_admin)
        await query.message.answer(text="Menyu",reply_markup=super_admin)
    else:
        await query.answer("Bekor qilindi")
        await query.bot.delete_message(chat_id=query.from_user.id,message_id=query.message.message_id)
        await query.message.answer(text="Menyu",reply_markup=super_admin)
    await state.clear()

#_______________________________________________FINISH_____________________________________________________________________________________________

#---------------------------"Adminni ishdan olish" funksiyasi---------------------------------------------------------------------------------#

#___________________________________________START_____________________________________________________________________________________________#

@super_admin_r.message(F.text == "Adminni ishdan olish")
async def del_admin(msg: Message, state:FSMContext):
    dbm = database.database_user(db_name)
    user = dbm.get_user(msg.from_user.id)
    if user[4] == 2:
        admins = dbm.get_all_admins()
        await msg.answer(text="Adminni tanlang ", reply_markup=admin_list_k(admins))
        await state.set_state(AdminState.delete_admin)
    else:
        await msg.answer(text="Buday menyu yo'q")

#---------------------------------------------------------------------------------------------------------------------------------------------#

@super_admin_r.message(AdminState.delete_admin)
async def admin(msg: Message, state: FSMContext):
    if msg.text == "Bekor qilish" or msg.text == "cancel":
        await msg.answer(text="Bekor qilindi.",reply_markup=super_admin)
        await state.clear()
    else:
        await msg.answer("Xatolik. Agar bekor qilmoqchi bo'sangiz 'cancel' yoki 'Bekor qilish' deb yuboring.")
# ---------------------------------------------------------------------------------------------------------------------------------------------#
@super_admin_r.callback_query(AdminState.delete_admin)
async def confirm_admin(query: CallbackQuery, state: FSMContext):
    await query.bot.delete_message(chat_id=query.from_user.id,message_id=query.message.message_id)
    if query.data == "Bekor qilish":
        await query.answer("Bekor qilindi.")
        await query.bot.delete_message(chat_id=query.from_user.id,message_id=query.message.message_id)
        await query.message.answer(text="Menyu",reply_markup=super_admin)
        await state.clear()
    else:
        dmb = database.database_user(db_name)
        user = dmb.get_user(int(query.data))
        info = f"Foydalanuvchi haqida ma'lumot\n\n\tIsm : {user[2]}\n\tTelegram id : {user[1]}\n\tUsername : @{user[5]}\nAdminlikdan olinsinmi ?"
        await query.message.answer(text=info, reply_markup=yes_or_noo)
        await state.update_data(tg_id=user[1])
        await state.set_state(AdminState.del_admin)


# ---------------------------------------------------------------------------------------------------------------------------------------------#
@super_admin_r.callback_query(AdminState.del_admin)
async def admin(query: CallbackQuery, state: FSMContext):
    dbm = database.database_user(db_name)
    data = await state.get_data()
    tg_id = data.get("tg_id")
    if query.data == "Ha":
        dbm.update_admin(tg_id=tg_id,new_admin_id=0)
        await query.answer("Admin ishdan bo'shatildi.")
        await query.bot.delete_message(chat_id=query.from_user.id,message_id=query.message.message_id)
        await query.bot.send_message(chat_id=tg_id,text="Siz ishdan bo'shatildingiz",reply_markup=menu)
        await query.message.answer(text="Menyu",reply_markup=super_admin)
    else:
        await query.answer("Bekor qilindi")
        await query.bot.delete_message(chat_id=query.from_user.id,message_id=query.message.message_id)
        await query.message.answer(text="Menyu",reply_markup=super_admin)
    await state.clear()

#_______________________________________________FINISH_____________________________________________________________________________________________

#---------------------------"Kanal Ulash" funksiyasi---------------------------------------------------------------------------------#

#___________________________________________START_____________________________________________________________________________________________#

@super_admin_r.message(F.text == "Kanal Ulash")
async def connect_channel(msg: Message, state: FSMContext):
    dbm = database.database_user(db_name)
    user = dbm.get_user(msg.from_user.id)
    if user[4] == 2:
        await msg.answer(text="Kanal havolasini yuboring.")
        await state.set_state(AdminState.c_channel)
    else:
        await msg.answer(text="Buday menyu yo'q")

#---------------------------------------------------------------------------------------------------------------------------------------------#

@super_admin_r.message(AdminState.c_channel)
async def sub_channel(msg: Message, state: FSMContext):
    await state.update_data(url = msg.text)
    await msg.answer(text="Kanal idsini yuboring")
    await state.set_state(AdminState.id_channel)

#---------------------------------------------------------------------------------------------------------------------------------------------#

@super_admin_r.message(AdminState.id_channel)
async def id_channel(msg: Message, state: FSMContext):
    try:
        channel_id = int(msg.text)
        await state.update_data(channel_id=channel_id)
        await msg.answer(text="Kanal nomini yuboring")
        await state.set_state(AdminState.name)
    except:
        await msg.answer(text="Id faqat sonlardan iborat bo'ladi")
        await state.set_state(AdminState.id_channel)

#---------------------------------------------------------------------------------------------------------------------------------------------#

@super_admin_r.message(AdminState.name)
async def id_channel(msg: Message, state: FSMContext):
    try:
        name = msg.text
        await state.update_data(name=name)
        data = await state.get_data()
        channel_id = data.get("channel_id")
        channel_url = data.get("url")
        await msg.answer(text=f"Kanal ma'lumotlarni teksiring:\n\tKanal havolasi : {channel_url}\n\tKanal idsi : {channel_id}\n\nKanal qo'shilsinmi?",reply_markup=yes_or_noo)
        await state.set_state(AdminState.verfy_channel_info)
    except:
        await msg.answer(text="Id faqat sonlardan iborat bo'ladi")

#---------------------------------------------------------------------------------------------------------------------------------------------#

@super_admin_r.callback_query(AdminState.verfy_channel_info)
async def verfy(query: CallbackQuery, state: FSMContext):
    if query.data == "Ha":
        db = database.database_channel(db_name)
        data = await state.get_data()
        channel_url = data.get("url")
        name = data.get("name")
        channel_id = data.get("channel_id")
        db.add_channel(channel_id=channel_id,url=channel_url, name=name)
        await query.answer(text="Kanal muvofaqqiyatli qo'shildi.")
        await query.bot.delete_message(chat_id=query.message.chat.id,message_id=query.message.message_id)
        await query.bot.send_message(chat_id=query.message.chat.id,text="Menu",reply_markup=super_admin)
        await state.clear()
    else:
        await query.answer(text="Bekor qilindi")
        await query.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        await query.bot.send_message(chat_id=query.message.chat.id, text="Menu", reply_markup=super_admin)
        await state.clear()

#_______________________________________________FINISH_______________________________________________________________________________________#

#---------------------------"Kanal ajratish" funksiyasi---------------------------------------------------------------------------------------#

#________________________________________________START________________________________________________________________________________________#


@super_admin_r.message(F.text == "Kanalni ajratish")
async def disconnect(msg: Message, state: FSMContext):
    dbm = database.database_user(db_name)
    dbch = database.database_channel(db_name)
    user = dbm.get_user(msg.from_user.id)
    channels = dbch.all_channel()
    if user[4] == 2:
        await msg.answer(text="Kanalni tanlang",reply_markup=channel_list_k(channels=channels))
        await state.set_state(AdminState.del_channel)
    else:
        await msg.answer(text="Buday menyu yo'q")

#---------------------------------------------------------------------------------------------------------------------------------------------#

@super_admin_r.callback_query(AdminState.del_channel)
async def del_confirm(msg: CallbackQuery, state: FSMContext):
    try:
        if msg.data != "Bekor qilish":
            await state.update_data(id=msg.data)
            db = database.database_channel(db_name)
            channel = db.get_channel(int(msg.data))
            if channel:
                await msg.bot.delete_message(msg.message.chat.id,message_id=msg.message.message_id)
                await msg.message.answer(text=f"Kanal haqida ma'lumot:\n\n\tKanal nomi : {channel[2]}\n\tKanal idisi : {channel[0]}\n\tKanal linki : {channel[1]}\n\nKanal ajratilsinmi?",reply_markup=yes_or_noo)
                await state.set_state(AdminState.del_ch)
            else:
                await msg.answer(text="Xatolik!",)
        else:
            await msg.answer(text="Bekor qilindi",reply_markup=super_admin)
            await msg.bot.delete_message(msg.message.chat.id,message_id=msg.message.message_id)
            await state.clear()
    except:
        await msg.answer("Id faqat sonlardan iborat bo'ladi. Qayta kiriting",reply_markup=bekor_qilish)

#---------------------------------------------------------------------------------------------------------------------------------------------#

@super_admin_r.callback_query(AdminState.del_ch)
async def del_channel(query: CallbackQuery,state: FSMContext):
    if query.data == "Ha":
        try:
            id = (await state.get_data()).get("id")
            db = database.database_channel(db_name)
            db.del_channel(id)
            await query.answer(text="Kanal muvoffaqiyatli ajratildi")
            await query.bot.delete_message(chat_id=query.message.chat.id,message_id=query.message.message_id)
            await query.message.answer(text="Menyu",reply_markup=super_admin)
            await state.clear()
        except:
            await query.message.answer(text="Nomalum xatolik qayta urunib ko'ring",reply_markup=super_admin)
    else:
        await query.answer(text="Bekor qilindi")
        await query.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        await query.message.answer(text="Menyu", reply_markup=super_admin)
        await state.clear()

#_______________________________________________FINISH_____________________________________________________________________________________________#


