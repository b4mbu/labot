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
from src.database.db_queries import check_token_role, create_user, create_lab, get_all_labs_as_one_string, is_admin, is_stud, is_exist_user, get_all_users_as_one_string, get_all_tokens_as_one_string, remove_token
from src.database.tokens import Token
from src.database.users import User
from src.database.variants import Variant
from src.database.users_variants import UserVariant
import aio_pika
import json
import asyncio


class Gen(StatesGroup):
    just_chill = State()

    # authentification 
    auth_wait_token     = State()
    auth_wait_full_name = State()

    # create lab 
    create_lab_wait_data = State()

    # remove token 
    token_remove_wait_token = State() 

    # choose variant
    variant_wait_name = State() 


dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Привет, я телеграм бот, который позволяет создавать и раздавать лабы студентам")
    await message.answer("Авторизуйтесь с помощью команды: /auth")
    await state.set_state(Gen.just_chill)

@dp.message(Command("help"))
async def cmd_help(message: types.Message, state: FSMContext):
    res = """
            Команды:
            /start - запустить бота
            /help - прочитать справочную информацию о боте
            /auth - авторизоваться
        """
    if is_admin(message.from_user.id):
        res = """
            Команды:
            /start - запустить бота
            /help - прочитать справочную информацию о боте
            /auth - авторизоваться
            /add_lab - создать новую лабораторную
            /show_labs - посмотреть список всех лаб
            /show_users - посмотреть всех пользователей
            /show_tokens - глянуть все токены (осторожно)
            /remove_token - удалить регистрационный токен
        """
    await message.answer(res)

@dp.message(Command("auth"))
async def cmd_authorization(message: types.Message, state: FSMContext):
    if is_exist_user(message.from_user.id):
        await message.answer("Вы уже авторизированы ;)")
        return
    await message.answer("Введите токен:")
    await state.set_state(Gen.auth_wait_token)

@dp.message(Command("add_lab"))
async def cmd_add_lab(message: types.Message, state: FSMContext):
    await message.answer("Введите данные лабораторной работы в формате:\n<название>\n\n<описание>")
    await state.set_state(Gen.create_lab_wait_data)

@dp.message(Command("show_labs"))
async def cmd_show_labs(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Пока нет доступа(")
        return
    labs = get_all_labs_as_one_string()
    if len(labs) == 0:
        await message.answer("Пока пусто!")
        return
    await message.answer(labs)

@dp.message(Command("show_users"))
async def cmd_show_users(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Пока нет доступа(")
        return
    users = get_all_users_as_one_string()
    if len(users) == 0:
        await message.answer("Пока пусто!")
        return
    await message.answer(users)

@dp.message(Command("show_tokens"))
async def cmd_show_tokens(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Пока нет доступа(")
        return
    tokens = get_all_tokens_as_one_string()
    if len(tokens) == 0:
        await message.answer("Пока пусто!")
        return
    await message.answer(tokens)

@dp.message(Command("remove_token"))
async def cmd_remove_token(message: types.Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Пока нет доступа(")
        return
    await message.answer("Введите токен, который нужно удалить: <token>")
    await state.set_state(Gen.token_remove_wait_token)



@dp.message(F.text, Gen.auth_wait_token)
async def check_token(message: types.Message, state: FSMContext):
    token = message.text
    response = json.loads(check_token_role(token))
    if response["status"] == "fail":
        await message.answer("Неверный токен")
        return
    await state.update_data(role=response["role"])
    await message.answer("Введите ФИО:")
    await state.set_state(Gen.auth_wait_full_name)

@dp.message(F.text, Gen.auth_wait_full_name)
async def auth_new_user(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    role = user_data["role"]
    create_user(message.text.lower().title(), role, message.from_user.id)
    await message.answer("Вход выполнен")
    await state.clear()    # удалит данные в state (user_data["role"]) -> removed

@dp.message(F.text, Gen.create_lab_wait_data)
async def create_new_lab(message: types.Message):
    text = message.text
    splitted = text.split('\n')
    name = splitted[0]
    description = '\n'.join(splitted[1:])
    if create_lab(name, description, message.from_user.id):
        await message.answer(f"Лабораторная работа \"{name}\" была создана")
        return
    await message.answer("Произошла ошибка")

@dp.message(F.text, Gen.token_remove_wait_token)
async def remove_token_from_table(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("Пока нет доступа(")
        return
    token = message.text.strip()
    if remove_token(token):
        await message.answer(f"Токен \"{token}\" был успешно удалён")
        return
    await message.answer("Неверный токен")



@dp.message(F.text.split(".").len() == 5)
async def get_date(message: types.Message):
    pass


@dp.message(F.text)
async def get_name(message: types.Message):
    import random

    # Создаем пустое поле для игры 3x3
    board = ["  " for _ in range(9)]

    # Функция для печати игрового поля
    def get_board():
        res = "_____\n"
        for i in range(3):
            res += "|" + "|".join(board[i*3:(i+1)*3]) + "|\n"
            if i < 2:
                res += "_____\n"
        return res

    # Функция для заполнения поля случайным образом
    def fill_board_randomly(board):
        # Случайное количество ходов для каждого символа
        num_moves = random.randint(3, 5)  # предполагаем, что будет от 3 до 5 ходов для каждого символа
        moves_done = 0
        while moves_done < num_moves:
            for symbol in ["X", "0"]:
                pos = random.randint(0, 8)
                if board[pos] == "  ":
                    board[pos] = symbol
                    moves_done += 1
                    if moves_done >= num_moves:
                        break

    # Заполним поле случайным образом и напечатаем его
    fill_board_randomly(board)
    board = get_board()
    await message.answer(board)


async def start_polling():
    bot = Bot(TelegramConfig().token)
    await bot.delete_webhook(drop_pending_updates=True)
    print("log: 200")
    await dp.start_polling(bot)

