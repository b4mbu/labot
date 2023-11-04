import json
from src.database import db_session
from config.config import RabbitMQConfig
import aio_pika
import asyncio
import traceback, sys


async def process_request(request):
    connection: aio_pika.RobustConnection = await aio_pika.connect_robust(
        f"amqp://{RabbitMQConfig().login}:{RabbitMQConfig().password}@{RabbitMQConfig().host}/")
    routing_key = "from_handler_to_bot"
    request = json.loads(request)
    channel: aio_pika.abc.AbstractChannel = await connection.channel()
    await channel.default_exchange.publish(aio_pika.Message(body=f'{request}'.encode()), routing_key=routing_key)
    await connection.close()


#if __name__ == "__main__":
async def handler_waiting():
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
        async with queue.iterator() as queue_iter:
            # Cancel consuming after __aexit__
            async for message in queue_iter:
                async with message.process():
                    await process_request(message.body.decode())
                    if queue.name in message.body.decode():
                        break

"""
type |        description                      
------------------------------------------      
   0 | узнать свой вариант на все лабы
   1 | узнать свой вариант/оценку/дедлайн по лабе Х
   2 | выбрать вариант на лабу Х 
   3 | поменять вариант по лабе Х
   4 |
   5 | 
   6 | 
   7 | посмотреть список всех вариантов по (группе/лабе/варианту)
   8 | посмотреть всеx пользователей с ролью У 
   9 | создать лабу Х
   10| выдать лабу Х (установить дедлайн, способ выдачи вариантов)
   11| создать вариант X для лабы У (возможно загрузить это файлом)
   12| создать токен для регистрации (кол-во активаций)
   13| удалить токен для регистрации
   14| удалить пользователя
"""

