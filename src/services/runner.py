import threading
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


    def run_one(self, flow_item, data):
        flow_performer = Flow(website=flow_item.get('website'), data=data)
        steps = flow_item.get('steps')
        for step in steps:
            name = step.get('name')
            step_flow = step.get('flow')
            print(step.get('skip_condition'))
            print(flow_performer.browser.skip_conditions)
            if len(step_flow) > 0 and not step.get('skip_condition') in flow_performer.browser.skip_conditions:
                print(f"[Step]:: Start step {name}")
                last_percentage = 0
                current_thread = threading.current_thread()
                for flow in step_flow:
                    error_in_step = self.is_current_thread_with_error_on_step(current_thread, flow_performer.threads_with_error)
                    if not error_in_step:
                        flow_performer.perform(name, flow, current_thread)
                        last_percentage = flow.get('percentage')
                    else:
                        break;
                if not error_in_step:
                    flow_performer.notify_end_of_step(name, last_percentage)
            print(f"[Step]:: End step {name}")
        
        flow_performer.finalize()

    def set_threads(self, data: dict):
        try:
            print(data)
            threads = []
            for flow_item in json.loads(self.flows):
                thread = threading.Thread(target=self.run_one, args=(flow_item, data,))
                threads.append(thread)

            for thread in threads:
                thread.start()

            return True
        except Exception as e:
            print(e)
            return False

    def is_current_thread_with_error_on_step(self, current_thread, threads_with_error):
        return current_thread.name in threads_with_error
