from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from DATA_BASE.database import database_channel
from config import db_name

reg = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Ro'yxatdan o'tish")]
],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Ro'yxatdan o'tish tugmasini bosing"
)

phone = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)]
],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='"Telefon raqamni yuborish" tugamsini bosing.'
)
menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Kino izlash"), KeyboardButton(text="Random kino")],
    [KeyboardButton(text="Botdagi kinolar ro'yxati"), KeyboardButton(text="ℹ️ Muallif haqida")]
],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Kerakli menuni tanlang"

)
kino_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Kod bo'yicha izlash"), KeyboardButton(text="Nom bo'yicha izlash")],
    [KeyboardButton(text="Orqaga")]
],
    resize_keyboard=True
)
orqaga = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Orqaga"), KeyboardButton(text="Menu")]
],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Agar menuga qaytmoqchi bo'lsangiz 'Menu' tugmasini bosing"

)
menu_admin = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Kino izlash"), KeyboardButton(text="Yangi kino yuklash")],
    [KeyboardButton(text="Xabar yuborish"), KeyboardButton(text="Random kino")],
    [KeyboardButton(text="Bot a'zolari soni"), KeyboardButton(text="ℹ️ Muallif haqida")]
],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Kerakli menuni tanlang"

)
yes_or_noo = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Ha", callback_data="Ha"),
        InlineKeyboardButton(text="Yo'q", callback_data="Yo'q")
    ]
])
janr = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Jangari", callback_data="jangar"),
        InlineKeyboardButton(text="Drama", callback_data="drama"),
        InlineKeyboardButton(text="Tarixiy", callback_data="tarixiy"),
        InlineKeyboardButton(text="Komediya", callback_data="komediya")
    ],
    [
        InlineKeyboardButton(text="Sarguzasht", callback_data="sarguzasht"),
        InlineKeyboardButton(text="Fantastika", callback_data="fantastik"),
        InlineKeyboardButton(text="Qo'rqinchli", callback_data="qorqinchli"),
        InlineKeyboardButton(text="Hayotiy", callback_data="hayotiy")
    ]
])
super_admin = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Yangi kino yuklash"), KeyboardButton(text="Kinoni olib tashlash")],
    [KeyboardButton(text="Kanal Ulash"), KeyboardButton(text="Kanalni ajratish")],
    [KeyboardButton(text="Yangi admin qo'shish"), KeyboardButton(text="Adminni ishdan olish")],
    [KeyboardButton(text="Xabar yuborish"), KeyboardButton(text="Bot a'zolari soni")]
],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Kerakli menuni tanlang"

)
bekor_qilish = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Bekor qilish")]
],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Agar bekor qilmoqchi bo'lsangiz 'Bekor qilish' tugmasini bosing."

)
yes_or_no_admin = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Ha(Super admin)", callback_data="super"),
        InlineKeyboardButton(text="Ha(Admin)", callback_data="admin"),
        InlineKeyboardButton(text="Yo'q", callback_data="Yo'q")
    ]
])


def follow_channel() -> InlineKeyboardMarkup:
    db = database_channel(db_name)
    channels = db.all_channel()
    rows = []
    for i in channels:
        rows.append([InlineKeyboardButton(text="Azo bo'lish", url=i[1])])
    rows.append([InlineKeyboardButton(text="Tekshirish", callback_data="tekshirish")])
    follow_channels = InlineKeyboardMarkup(inline_keyboard=rows)
    return follow_channels


left_right_k = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️", callback_data="left"),
     InlineKeyboardButton(text="➡️", callback_data="right")],
])


# def movies_list_k(interval: list):
#     rows = []
#     row = []
#     n = 1
#     a = 0
#     for i in range(interval[0], interval[1]):
#         if len(row) == 5:
#             rows.append(row)
#             if a == 0:
#             	row = [InlineKeyboardButton(text=str(n), callback_data=str(i))]
#             elif a == 1:
#             	break
#             a += 1
#         else:
#             row.append(InlineKeyboardButton(text=str(n), callback_data=str(i)))
#         n += 1
#     else:
#         rows.append(row)
#     rows.append([InlineKeyboardButton(text="⬅️", callback_data="left"),
#              InlineKeyboardButton(text="➡️", callback_data="right")])
#     movies_list = InlineKeyboardMarkup(inline_keyboard=rows)
#     return movies_list


def admin_list_k(admins: dict):
    rows = []
    for i in admins:
        rows.append([InlineKeyboardButton(text=f"{i[2]} {i[4]}", callback_data=str(i[1]))])
    rows.append([InlineKeyboardButton(text="Bekor qilish", callback_data="Bekor qilish")])
    movies_list = InlineKeyboardMarkup(inline_keyboard=rows)
    return movies_list


def channel_list_k(channels: dict):
    rows = []
    for i in channels:
        rows.append([InlineKeyboardButton(text=f"{i[2]}", callback_data=str(i[0]))])
    rows.append([InlineKeyboardButton(text="Bekor qilish", callback_data="Bekor qilish")])
    channel_list = InlineKeyboardMarkup(inline_keyboard=rows)
    return channel_list
