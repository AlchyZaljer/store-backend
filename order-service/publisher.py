import json

import pika


RABBITMQ_HOST = "localhost"
RABBITMQ_QUEUE = "notifications"

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)


def publish_to_rabbitmq(message: dict):
    try:
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=1,
            )
        )

        print(f"Publish order {message['id']} notification")
    except Exception as e:
        print(f"Error while publishing message to RabbitMQ: {e}")
    finally:
        if connection:
            connection.close()
