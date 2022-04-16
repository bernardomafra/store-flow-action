from src.services.flow import Flow
from src.services.rabbitmq_producer import RabbitMQProducer
from src.services.rabbitmq_consumer import RabbitMQConsumer
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
        steps = flow_item.get('steps')
        for step in steps:
            name = step.get('name')
            step_flow = step.get('flow')
            if len(step_flow) > 0:
                print(f"[Step]:: Start step {name}")
                for flow in step_flow:
                    flow_performer.perform(flow)
                print(f"[Step]:: End step {name}")

        flow_performer.finalize()


    def run(self):
        for flow_item in json.loads(self.flows):
            self.run_one(flow_item)

