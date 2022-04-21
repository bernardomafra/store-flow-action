import logging
import time
from src.services.chrome import Chrome
from src.custom_types import FlowData
from src.services.rabbitmq_producer import RabbitMQProducer


class Flow:
    website = ""
    browser = ""
    step_queue = ""

    def __init__(self, website, product):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | [%(name)s - %(levelname)s] | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger("Flow")

        self.website = website
        self.logger.info(f"Flow initialized for website {website}")
        self.browser = Chrome(product)
        try:
            self.step_queue = RabbitMQProducer()
        except Exception as e:
            self.logger.error('Error at RabbitMQProducer: "{}"'.format(e))
            self.browser.end_connection()
            exit(1)


    def perform(self, flow_data: FlowData):
        successfully_performed = False
        if not self.is_flowdata_valid(flow_data) or not self.website:
            return successfully_performed

        flow_data_step = flow_data.get("step")

        self.browser.open(self.website)
        self.browser.get_element_and_add_actions(
            flow_data.get("key_type"),
            flow_data.get("key"),
            flow_data.get("action"),
            flow_data_step
        )
        self.browser.perform_actions()
        if self.browser.has_error_in_step(step=flow_data_step):
            self.notify_step(flow_data_step, flow_data.get("percentage"), error="error")
        else:
            self.notify_step(flow_data_step, flow_data.get('percentage'))

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

    def notify_step(self, step: str, percentage: int, error: str = ""):
        if (error):
            self.step_queue.send_message(self.website, f"Error at: {step}", 0, self.browser.get_current_url())
        else:
            self.step_queue.send_message(self.website, f"Step: {step}", percentage, self.browser.get_current_url())
        
    def finalize(self):
        self.browser.end_connection()
        self.step_queue.close_connection()