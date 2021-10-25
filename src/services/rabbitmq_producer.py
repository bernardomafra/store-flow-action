import pika
import logging
import json
import random


class RabbitMQProducer:
    queue = "hello_world"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | [%(name)s - %(levelname)s] | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("pika").setLevel(logging.WARNING)

    def __init__(self, host, port):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host, port))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.logger = logging.getLogger("RabbitMQ")

    def send_message(self, website, text):
        body = {"website": website, "step": text, "percentage": random.randint(10, 100)}
        self.channel.basic_publish(
            exchange="", routing_key=self.queue, body=json.dumps(body)
        )
        self.logger.info(f"Message Sent :: {text}")

    def close_connection(self):
        self.channel.close()
        self.connection.close()
