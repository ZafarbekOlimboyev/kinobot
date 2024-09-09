from aiogram.fsm.state import State,StatesGroup

class RegistrState(StatesGroup):
    regPhone = State()
    find_kino = State()
    menu = State()
    regs = State()
    admin_mode = State()
    random = State()
    channel = State()
    kino_name = State()
    kino_code = State()
    kino = State()
    kino_list = State()
