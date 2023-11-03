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
        fl = 1
        async with queue.iterator() as queue_iter:
            # Cancel consuming after __aexit__
            async for message in queue_iter:
                async with message.process():
                    await process_request(message.body.decode())
                    if queue.name in message.body.decode():
                        break
    await connection.close()
