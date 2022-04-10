from services.flow import Flow
from services.rabbitmq_producer import RabbitMQProducer
from services.rabbitmq_consumer import RabbitMQConsumer
import json


class Runner:
    producerQueue = RabbitMQProducer()
    flows = {}

    def __init__(self, flows):
        self.flows = flows

    try:
        queue = RabbitMQConsumer()
    except Exception as e:
        print(e)
        exit(1)


    def run_one(self, flow_item):
        flow_performer = Flow(flow_item.get('website'))
        flow_steps = flow_item.get('steps')
        for step in flow_steps:
            flow_performer.perform(step)


    def run(self):
        for flow_item in json.loads(self.flows):
            self.run_one(flow_item)

