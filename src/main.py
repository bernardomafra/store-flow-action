from services.flow import Flow
from services.rabbitmq_producer import RabbitMQProducer
from services.rabbitmq_consumer import RabbitMQConsumer

producerQueue = RabbitMQProducer()
data = {}
try:
    queue = RabbitMQConsumer()
    data = queue.get()
except Exception as e:
    print(e)
    exit(1)

processes = []

actions = data.get("actions")


def run_one(website):
    flow_performer = Flow(website)
    flows = actions.get(website).get("flow")
    for flow_data in flows:
        flow_performer.perform(flow_data)


def run():
    for website, _ in actions.items():
        run_one(website)


run()
