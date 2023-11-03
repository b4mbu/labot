import asyncio
from src.telegram import telegram
from src.database import db_session, database_scheme
from config.config import DatabaseConfig
from src.queue.handler import handler_waiting
from concurrent.futures import ProcessPoolExecutor


async def main():
    q = asyncio.create_task(telegram.from_queue())
    b = asyncio.create_task(telegram.start_polling())
    p = asyncio.create_task(handler_waiting())
    await q
    print("hello world")
    await b
    print("lol")
    await p


if __name__ == "__main__":
    db_session.global_init()
    asyncio.run(main())

    # asyncio.run(telegram.start_polling())
