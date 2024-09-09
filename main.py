import sys
from config import TOKEN
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
import asyncio
import logging
from hendlers.cmd_c import cmd_co
from hendlers.msg_c import msg_co
from hendlers.admin import admin_co
from hendlers.super_admin import super_admin_r
from aiogram.client.session.aiohttp import AiohttpSession

async def main():
    # PROXY = 'http://proxy.server:3128/'
    # session = AiohttpSession(proxy=PROXY)
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    await bot.set_my_commands(commands=[
        BotCommand(command="start", description="Botni qayta ishga tushurish")
    ])
    dp.include_routers(cmd_co,admin_co,super_admin_r, msg_co)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
