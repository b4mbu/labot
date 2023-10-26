import asyncio
from src.telegram import telegram
from src.database import db_session, database_scheme
from config import config
from concurrent.futures import ProcessPoolExecutor


async def main():
    q = asyncio.create_task(telegram.from_queue())
    b = asyncio.create_task(telegram.start_polling())
    await q
    print("hello world")
    await b


if __name__ == "__main__":
    config = config.Config()
    asyncio.run(main())

    # db_session.global_init(config.database)
    # asyncio.run(telegram.start_polling())
