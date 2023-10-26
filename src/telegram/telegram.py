from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from config import config
from time import sleep
from src.database import db_session
from src.database.labs import Lab
from src.database.tokens import Token
from src.database.users import User
from src.database.variants import Variant
from src.database.users_variants import UserVariant
import pika
import json
import asyncio

dp = Dispatcher()

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


async def listener(message):
    print("I go sleep")
    await asyncio.sleep(10)
    await message.reply("I am wake up")
    print("Wake up")
    pass


@dp.message(F.text)
async def type_of_responce(message: types.Message):
    await listener(message)
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
