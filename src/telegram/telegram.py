from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from config.config import TelegramConfig
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from src.database.db_queries import (
    check_token_role,
    create_user,
    create_lab,
    get_all_labs_as_one_string,
    is_admin,
    is_exist_user,
    get_all_users_as_one_string,
    get_all_tokens_as_one_string,
    remove_token,
)
import json


class Gen(StatesGroup):
    just_chill = State()

    # authentification
    auth_wait_token = State()
    auth_wait_full_name = State()

    # create lab
    lab_create_wait_name = State()
    lab_create_wait_description = State()

    # create variant
    variant_create_wait_lab_name = State()
    variant_create_wait_name = State()
    variant_create_wait_descruption = State()

    # remove token
    token_remove_wait_token = State()

    # choose variant
    variant_wait_name = State()


dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(
        "Привет, я телеграм бот, который позволяет создавать и раздавать лабы студентам"
    )
    await message.answer("Авторизуйтесь с помощью команды: /auth")
    await state.set_state(Gen.just_chill)


@dp.message(Command("help"))
async def cmd_help(message: types.Message, state: FSMContext):
    res = """
            Команды:
            /start - запустить бота
            /help - прочитать справочную информацию о боте
            /auth - авторизоваться
            /show_vars - посмотреть список вариантов одной лабы
        """
    if is_admin(message.from_user.id):
        res = """
            Команды:
            /start - запустить бота
            /help - прочитать справочную информацию о боте
            /auth - авторизоваться
            /add_lab - создать новую лабораторную
            /show_labs - посмотреть список всех лаб
            /show_vars - посмотреть список вариантов одной лабы
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
    await message.answer("Введите название лабораторной работы")
    await state.set_state(Gen.lab_create_wait_name)


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

@dp.message(Command("show_vars"))
async def cmd_show_vars(message: types.Message, state: FSMContext):
    await message.answer("Введите название лабы, у которой нужно посмотреть варианты: <название>")
    await state.set_state(Gen.show_var_wait_lab_name)

@dp.message(F.text, Gen.auth_wait_token)
async def check_token(message: types.Message, state: FSMContext):
    token = message.text
    response = json.loads(check_token_role(token))
    if response["status"] == "fail":
        await message.answer("Неверный токен, попробуйте другой")
        return
    await state.update_data(role=response["role"])
    await message.answer("Введите ФИО:")
    await state.set_state(Gen.wait_full_name)


@dp.message(F.text, Gen.auth_wait_full_name)
async def auth_new_user(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    role = user_data["role"]
    create_user(message.text.lower().title(), role, message.from_user.id)
    await message.answer("Вход выполнен")
    await state.clear()  # удалит данные в state (user_data["role"]) -> removed


@dp.message(F.text, Gen.lab_create_wait_name)
async def create_new_lab_get_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await state.set_state(Gen.lab_create_wait_description)
    await message.answer("Введите описание лабораторной работы")


@dp.message(F.text, Gen.lab_create_wait_description)
async def create_new_lab_get_description(message: types.Message, state: FSMContext):
    description = message.text
    user_data = await state.get_data()
    name = user_data["name"]
    if create_lab(name, description, message.from_user.id):
        await message.answer(f"Лабораторная работа \"{name}\" была создана")
        await state.clear()
        return
    await message.answer("Произошла ошибка")
    await state.clear()


@dp.message(F.text, Gen.token_remove_wait_token)
async def remove_token_from_table(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("Пока нет доступа(")
        return
    token = message.text.strip()
    if remove_token(token):
        await message.answer(f"Токен \"{token}\" был успешно удалён")
        await state.clear()
        return
    await message.answer("Неверный токен")

@dp.message(F.text, Gen.show_var_wait_lab_name)
async def show_variants(message: types.Message, state: FSMContext):
    variants = get_variants_for_lab(message.text)
    if len(variants) == 0:
        await message.answer("Пока пусто!")
        await state.clear()
        return
    await message.answer(variants)
    await state.clear()


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
            res += "|" + "|".join(board[i * 3 : (i + 1) * 3]) + "|\n"
            if i < 2:
                res += "_____\n"
        return res

    # Функция для заполнения поля случайным образом
    def fill_board_randomly(board):
        # Случайное количество ходов для каждого символа
        num_moves = random.randint(
            3, 5
        )  # предполагаем, что будет от 3 до 5 ходов для каждого символа
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
