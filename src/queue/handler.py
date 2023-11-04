from src.database import db_session
from config.config import RabbitMQConfig
import src.database.db_queries
import json
import aio_pika
import asyncio
import traceback
import sys

"""
type |  description    |  request format | response format                  
-----------------------------------------------------------
   0 | проверить Token |  {token: str}   | {status: [ok/fail],
                                            role: str}
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


async def process_request(request):
    aio_pika.RobustConnection = await aio_pika.connect_robust(
        f"amqp://{RabbitMQConfig().login}:{RabbitMQConfig().password}@{RabbitMQConfig().host}/")
    aio_pika.abc.AbstractChannel = await connection.channel()

    routing_key = "from_handler_to_bot"
    request = json.loads(request)
    response = json.dumps({"status": "fail"})
    print("get :", request)
    print("type" in request.keys())
    print(request["type"] == 1)
    print(request["token"])
    xxx = check_token_role("ksdghkghsaskgjh90000")
    print(xxx)
    print("fff")
    if "type" in request:
        if request["type"] == 0:
            response = add_new_token(request["role"], request["count_of_activation"])
        elif request["type"] == 1:
            response = check_token_role(request["token"])
        else:
            response = response

    print("procces:", response)
    
    await channel.default_exchange.publish(aio_pika.Message(body=response.encode()), routing_key=routing_key)
    await connection.close()


#if __name__ == "__main__":
async def handler_waiting():
    print("h1")
    connection = await aio_pika.connect_robust(
        f"amqp://{RabbitMQConfig().login}:{RabbitMQConfig().password}@{RabbitMQConfig().host}/"
    )

    async with connection:
        print("h2")
        queue_name = "from_bot_to_handler"
        # Creating channel
        channel: aio_pika.abc.AbstractChannel = await connection.channel()

        # Declaring queue
        queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(
            queue_name,
            auto_delete=True
        )
        async with queue.iterator() as queue_iter:
            print("h3")
            # Cancel consuming after __aexit__
            async for message in queue_iter:
                print("h4")
                async with message.process():
                    print("h5")
                    await process_request(message.body.decode())
                    if queue.name in message.body.decode():
                        break

