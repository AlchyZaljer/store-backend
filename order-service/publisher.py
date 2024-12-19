import json
import os

import pika


RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
RABBITMQ_QUEUE = "notifications"

connection = None
channel = None


def get_connection():
    global connection, channel
    if not connection or connection.is_closed:
        connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    return channel


def publish_to_rabbitmq(message: dict):
    try:
        global channel
        channel = get_connection()
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )
        print(f"Publish order {message['id']} notification")
    except Exception as e:
        print(f"Error while publishing message to RabbitMQ: {e}")

        if connection and connection.is_open:
            connection.close()
