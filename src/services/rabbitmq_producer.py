import pika
import logging
import json
import random


class RabbitMQProducer:
    queue = "store-flow-steps"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | [%(name)s - %(levelname)s] | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("pika").setLevel(logging.WARNING)

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.URLParameters('amqps://ybbzaglt:UqYv8vCBOVDUEZez0q03b_v0VPXFO22Q@moose.rmq.cloudamqp.com/ybbzaglt')
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.logger = logging.getLogger("RabbitMQ")

    def send_message(self, website, text, percentage):
        body = {"website": website, "step": text, "percentage": percentage}
        self.channel.basic_publish(
            exchange="", routing_key=self.queue, body=json.dumps(body)
        )
        self.logger.info(f"Message Sent :: {text}")

    def close_connection(self):
        self.channel.close()
        self.connection.close()
