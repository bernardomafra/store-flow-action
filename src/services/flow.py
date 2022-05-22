import logging
import time
from src.services.chrome import Chrome
from src.custom_types import FlowData
from src.services.rabbitmq_producer import RabbitMQProducer


class Flow:
    website = ""
    browser = ""
    step_queue = ""
    threads_with_error = []
    is_website_open = False

    def __init__(self, website, data):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | [%(name)s - %(levelname)s] | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger("Flow")

        self.website = website
        self.logger.info(f"Flow initialized for website {website}")
        self.browser = Chrome(variables=data)
        try:
            self.step_queue = RabbitMQProducer()
        except Exception as e:
            self.logger.error('Error at RabbitMQProducer: "{}"'.format(e))
            self.browser.end_connection()
            exit(1)


    def perform(self, step_name:str, flow_data: FlowData, thread):
        successfully_performed = False
        if not self.is_flowdata_valid(flow_data) or not self.website:
            return successfully_performed

        flow_data_step = flow_data.get("step")

        if not self.is_website_open:
            self.browser.open(self.website)
            self.is_website_open = True
        self.browser.get_element_and_add_actions(
            flow_data.get("key_type"),
            flow_data.get("key"),
            flow_data.get("action"),
            flow_data_step
        )
        self.browser.perform_actions()
        if self.browser.has_error_in_step(step=flow_data_step):
            self.threads_with_error.append(thread.name)
            self.logger.error(f'Thread error {thread.name} in step {step_name}')
            self.notify_step(step_name, flow_data_step, flow_data.get("percentage"), error="error")
        else:
            self.notify_step(step_name, flow_data_step, flow_data.get('percentage'))

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

    def notify_step(self, step_name:str,  step: str, percentage: int, error: str = ""):
        if (error):
            self.browser.driver.save_screenshot(f"{step_name}-{step}-{percentage}.png")
            self.logger.error(f'Error in step {step_name}: {error}')
            self.step_queue.send_message(self.website, f"Error at: {step}", 0, self.browser.get_current_page_title(), self.browser.get_current_url())
        else:
            if percentage == 90:
                self.browser.driver.save_screenshot(f"{step_name}-{percentage}.png")
            self.step_queue.send_message(self.website, f"{step_name}: {step}", percentage, self.browser.get_current_page_title(), self.browser.get_current_url())
        
    def notify_end_of_step(self, step_name:str, percentage: int):
        self.notify_step(step_name, "Finalizado", percentage)

    def finalize(self):
        self.is_website_open = False
        self.browser.end_connection()
        self.step_queue.close_connection()