from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import config
from config.config import TelegramConfig, RabbitMQConfig
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

dp = Dispatcher()
global_rmq_config = ""

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет, я телеграм бот, который позволяет создавать и раздавать лабы студентам")
    await message.answer("Авторизуйтесь с помощью команды: /auth")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("""
Команды:
/start - запустить бота
/help - прочитать справочную информацию о боте
/auth - авторизоваться
""")


f = '''
@dp.message(Command("auth"))
async def cmd_authorization(message: types.Message):
    await message.answer("Введите токен:")

    @dp.message(F.text)
    async def check_token(message: types.Message):
        connection_params = pika.ConnectionParameters('localhost', 5672)
        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()

        channel.queue_declare(queue="from_bot_to_handler", durable=True)
        channel.basic_publish(exchange='',
                              routing_key='from_bot_to_handler',
                              body=json.dumps([message.chat.id,
                                               user_currency,
                                               user_limit,
                                               user_bank,
                                               user_stock_markets]),
                              properties=pika.BasicProperties(
                                  delivery_mode=2
                              ))
        markup = types.ReplyKeyboardMarkup()
        buttons = [START_OVER_BUTTON, HELP_BUTTON]
        markup.add(*buttons)
        mess = 'Работаем...'
        bot.send_message(message.chat.id, mess, reply_markup=markup)
        connection.close()
'''


async def from_queue():
    connection = await aio_pika.connect_robust(
        f"amqp://{RabbitMQConfig().login}:{RabbitMQConfig().password}@{RabbitMQConfig().host}/"
    )

    async with connection:
        queue_name = "from_bot_to_handler"
        # Creating channel
        channel: aio_pika.abc.AbstractChannel = await connection.channel()

        # Declaring queue
        queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(
            queue_name,
            auto_delete=True
        )
        fl = 1
        async with queue.iterator() as queue_iter:
            # Cancel consuming after __aexit__
            async for message in queue_iter:
                async with message.process():
                    print(message.body.decode())

                    if queue.name in message.body.decode():
                        break
    print("close")


async def to_queue(message):
    connection: aio_pika.RobustConnection = await aio_pika.connect_robust(f"amqp://{RabbitMQConfig().login}:{RabbitMQConfig().password}@{RabbitMQConfig().host}/")
    routing_key = "from_bot_to_handler"
    channel: aio_pika.abc.AbstractChannel = await connection.channel()
    await channel.default_exchange.publish(aio_pika.Message(body=f'{message.text}'.encode()), routing_key=routing_key)
    await connection.close()


@dp.message(F.text)
async def type_of_responce(message: types.Message):
    await to_queue(message)
    pass


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

