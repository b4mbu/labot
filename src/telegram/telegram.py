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
from src.database.tokens import Token
from src.database.users import User
from src.database.variants import Variant
from src.database.users_variants import UserVariant
import aio_pika
import json
import asyncio


class Gen(StatesGroup):
    just_chill = State()
    wait_token = State()


dp = Dispatcher()
global_rmq_config = ""


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    print(message.chat.id)
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
""")


@dp.message(Command("auth"))
async def cmd_authorization(message: types.Message, state: FSMContext):
    await message.answer("Введите токен:")
    await state.set_state(Gen.wait_token)


@dp.message(F.text, Gen.wait_token)
async def check_token(message: types.Message):
    await to_queue(json.dumps({"type": 1, "token": message.text}))


async def from_queue():
    print("s")
    connection = await aio_pika.connect_robust(
        f"amqp://{RabbitMQConfig().login}:{RabbitMQConfig().password}@{RabbitMQConfig().host}/"
    )

    async with connection:
        print("s1")
        queue_name = "from_handler_to_bot"
        # Creating channel
        channel: aio_pika.abc.AbstractChannel = await connection.channel()

        # Declaring queue
        queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(
            queue_name,
            auto_delete=True
        )
        
        async with queue.iterator() as queue_iter:
            # Cancel consuming after __aexit__
            print("s2")
            async for message in queue_iter:
                print("s3")
                async with message.process():
                    print(1, message.body.decode())

                    if queue.name in message.body.decode():
                        break


async def to_queue(message):
    connection: aio_pika.RobustConnection = await aio_pika.connect_robust(f"amqp://{RabbitMQConfig().login}:{RabbitMQConfig().password}@{RabbitMQConfig().host}/")
    routing_key = "from_bot_to_handler"
    channel: aio_pika.abc.AbstractChannel = await connection.channel()
    await channel.default_exchange.publish(aio_pika.Message(body=message.encode()), routing_key=routing_key)
    await connection.close()
    print("added to queue", message)


@dp.message(F.text)
async def type_of_responce(message: types.Message):
    print("here", message.text)
    await to_queue(json.dumps({"type": 1, "token": message.text}))
    #a = message.text.split()
    #await to_queue(json.dumps({"type": 0, "role": a[0], "count_of_activation": a[1]}))


@dp.message(F.text.split(".").len() == 5)
async def get_date(message: types.Message):
    pass


async def start_polling():
    bot = Bot(TelegramConfig().token)
    await bot.delete_webhook(drop_pending_updates=True)
    print("log: 200")
    await dp.start_polling(bot)

