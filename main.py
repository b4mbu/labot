"""
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
    db_session.global_init(DatabaseConfig())
    asyncio.run(main())

    # asyncio.run(telegram.start_polling())
"""

from config import config
from src.database import db_session
from src.database.labs           import Lab
from src.database.tokens         import Token
from src.database.users          import User
from src.database.variants       import Variant
from src.database.users_variants import UserVariant
from src.database.db_queries import *


db_session.global_init()


session = db_session.create_session()
for x in session.query(User).all():
    print(x)

print("-"*10)
#print(generate_token("usr", 10))

for x in session.query(Token).all():
    print(x)

session.close()

create_user('{"role": "adm", "full_name": "Ткаченко Егор Юрьевич", "telegram_id":1146620547}')


"""
tmp = Token()
session.add(tmp)
session.commit()
x = session.query(User).filter(User.id == 10).all()
print(x)
print(type(x))

"""
