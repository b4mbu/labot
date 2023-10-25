from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio


bot = Bot("6924590259:AAH2mm_f46UQTudJwzqjuF6iTXJl1OqFz1M")
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
async def cmd_help(message: types.Message):
    await message.answer("""Введите в одном сообщении но на разных строках имя вашего аккаунта и пароль""")

@dp.message(F.text.isdigit())
async def type_of_responce(message: types.Message):
    pass


@dp.message(F.text.split(".").len() == 5)
async def get_date(message: types.Message):
    pass


@dp.message(F.text)
async def get_name(message: types.Message):
    pass


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
