from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import config
from config.config import TelegramConfig, RabbitMQConfig
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from time import sleep
from src.database import db_session
from src.database.labs import Lab
from src.database.db_queries import check_token_role, create_user, create_lab, get_all_labs, is_admin, is_stud, is_exist_user
from src.database.tokens import Token
from src.database.users import User
from src.database.variants import Variant
from src.database.users_variants import UserVariant
import aio_pika
import json
import asyncio


class Gen(StatesGroup):
    just_chill     = State()
    wait_token     = State()
    wait_full_name = State()
    wait_lab_data  = State()


dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Привет, я телеграм бот, который позволяет создавать и раздавать лабы студентам")
    await message.answer("Авторизуйтесь с помощью команды: /auth")
    await state.set_state(Gen.just_chill)


@dp.message(Command("help"))
async def cmd_help(message: types.Message, state: FSMContext):
    await message.answer("""
Команды:
/start - запустить бота
/help - прочитать справочную информацию о боте
/auth - авторизоваться
/add_lab - создать новую лабораторную
""")


@dp.message(Command("auth"))
async def cmd_authorization(message: types.Message, state: FSMContext):
    if is_exist_user(message.from_user.id):
        await message.answer("Вы уже авторизированы ;)")
        return
    await message.answer("Введите токен:")
    await state.set_state(Gen.wait_token)


@dp.message(Command("add_lab"))
async def cmd_add_lab(message: types.Message, state: FSMContext):
    await message.answer("Введите данные лабораторной работы в формате:\n<название>\n\n<описание>")
    await state.set_state(Gen.wait_lab_data)

@dp.message(Command("show_labs"))
async def cmd_add_lab(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Пока нет доступа(")
        return
    labs = get_all_labs()
    await message.answer(labs)

@dp.message(F.text, Gen.wait_token)
async def check_token(message: types.Message):
    token = message.text
    response = json.loads(check_token_role(token))
    if response["status"] == "fail":
        await message.answer("Неверный токен")
        return
    role = response["role"]
    create_user(message.from_user.id, role, message.from_user.id)
    await message.answer("Вход выполнен")

@dp.message(F.text, Gen.wait_lab_data)
async def create_new_lab(message: types.Message):
    text = message.text
    splitted = text.split('\n')
    name = splitted[0]
    description = '\n'.join(splitted[1:])
    if create_lab(name, description, message.from_user.id):
        await message.answer(f"Лабораторная работа \"{name}\" была создана")
        return
    await message.answer("Произошла ошибка")


@dp.message(F.text)
async def type_of_response(message: types.Message):
    print(message.text)



@dp.message(F.text.split(".").len() == 5)
async def get_date(message: types.Message):
    pass


@dp.message(F.text)
async def get_name(message: types.Message):
    pass


async def start_polling():
    bot = Bot(TelegramConfig().token)
    await bot.delete_webhook(drop_pending_updates=True)
    print("log: 200")
    await dp.start_polling(bot)

