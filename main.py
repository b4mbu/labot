import asyncio
from src.telegram import telegram
from src.database import db_session, database_scheme
from config.config import DatabaseConfig
from src.queue.handler import handler_waiting
from concurrent.futures import ProcessPoolExecutor


async def main():
    b = asyncio.create_task(telegram.start_polling())
    await b


if __name__ == "__main__":
    db_session.global_init()
    asyncio.run(main())
