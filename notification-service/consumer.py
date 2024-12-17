import json
from datetime import datetime

import pika

from database import get_db
from models import Notification

db = next(get_db())

RABBITMQ_HOST = "localhost"
RABBITMQ_QUEUE = "notifications"

connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)


def start_consumer():
    def callback(ch, method, properties, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        data = json.loads(body)
        notification = Notification(
            id=data['id'],
            message="Order completed",
            timestamp=datetime.now(),
        )
        db.notifications.insert_one(notification.model_dump())

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    connection.close()


if __name__ == "__main__":
    start_consumer()
