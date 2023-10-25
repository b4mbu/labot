from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import config
from src.database import db_session
from src.database.labs import Lab
from src.database.tokens import Token
from src.database.users import User
from src.database.variants import Variant
from src.database.users_variants import UserVariant
import asyncio

dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет, я телеграм бот, который позволяет создавать и раздавать лабы студентам")
    await message.answer("Авторизуйтесь с помощью команды: /authorization")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("""
Команды:
/start - запустить бота
/help - прочитать справочную информацию о боте
/authorization - авторизоваться
""")


@dp.message(Command("authorization"))
async def cmd_authorization(message: types.Message):
    ans = message.text
    print(ans)


@dp.message(F.text.isdigit())
async def type_of_responce(message: types.Message):
    pass


@dp.message(F.text.split(".").len() == 5)
async def get_date(message: types.Message):
    pass


@dp.message(F.text)
async def get_name(message: types.Message):
    pass


async def start_polling(config : config.TelegramConfig):
    bot = Bot(config.token)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    print("log: 200")
