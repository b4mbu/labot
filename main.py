import asyncio
from src.telegram import telegram
from src.database import db_session
from config import config

if __name__ == "__main__":
    config = config.Config() 

    db_session.global_init(config.database)
    asyncio.run(telegram.start_polling(config.telegram))
