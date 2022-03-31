import logging
from services.chrome import Chrome
from custom_types import FlowData
from services.rabbitmq_producer import RabbitMQProducer


class Flow:
    website = ""
    browser = ""
    step_queue = ""

    def __init__(self, website):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | [%(name)s - %(levelname)s] | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger("Flow")

        self.website = website
        self.logger.info(f"Flow initialized for website {website}")
        self.browser = Chrome(headless=False)
        try:
            self.step_queue = RabbitMQProducer(host="localhost", port=5672)
        except Exception as e:
            self.logger.error('Error at RabbitMQProducer: "{}"'.format(e))
            exit(1)


    def perform(self, flow_data: FlowData):
        successfully_performed = False
        if not self.is_flowdata_valid(flow_data) or not self.website:
            return successfully_performed

        self.browser.open(self.website)
        self.browser.get_element_and_add_actions(
            flow_data.get("key_type"),
            flow_data.get("key"),
            flow_data.get("action"),
        )
        self.browser.perform_actions()
        self.notify_step(flow_data.get('step'))

    def is_flowdata_valid(self, flow_data: FlowData):
        has_keys = len(flow_data) >= 0
        has_key_type = flow_data.get("key_type")
        has_key = flow_data.get("key")
        has_step = flow_data.get("step")
        has_action = flow_data.get("action")

        if has_keys and has_key and has_key_type and has_step and has_action:
            self.logger.info("Flow valid")
            return True

        return False

    def notify_step(self, step: str):
        self.step_queue.send_message(self.website, f"Step: {step}")
        