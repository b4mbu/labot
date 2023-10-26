import json
from src.database import db_session
import pika
import traceback, sys

if __name__ == "__main__":
    db_session.global_init()

    connection_parameters = pika.ConnectionParameters('localhost', 15672)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue="from_bot_to_handler", durable=True)
    channel.queue_declare(queue="from_handler_to_bot")


    def callback(ch, method, properties, body):
        requests_body = json.loads(body)
        # [message.chat.id,request_type,message]
        chat_id = requests_body[0]
        request_type = requests_body[1]
        message = requests_body[2]
        # ТО ЧТО ОТПРАВЛЕТЕ В БОТА ОБРАТНО
        answer_message = ""
        db = db_session.create_session()
        if request_type == 1:
            pass
        elif request_type == 2:
            pass


        channel.basic_publish(exchange='',
                              routing_key='from_parser_to_bot',
                              body=json.dumps([chat_id, answer_message]),
                              properties=pika.BasicProperties(
                                  delivery_mode=2
                              ))


    channel.basic_consume(callback, queue="from_bot_to_handler")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    except Exception:
        channel.stop_consuming()
        traceback.print_exc(file=sys.stdout)

    channel.close()
