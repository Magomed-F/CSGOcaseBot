from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from environs import Env
import asyncio


from core.handlers import user, admin
from core.keyboards import user_inline_kb, admin_kb
from core.filters import InGroupCheck
from core.db import dbconnect, info, case_content, cases, support, withdraws, prices
from core.utils import states

env = Env()

env.read_env()


token = env('token')


async def start() -> None:
    bot = Bot(token=token)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(user.router)
    dp.include_router(admin.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())

