import os
from random import randint
from src.custom_types import Action

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from src.services.actions import Actions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from src.utils import Utils
from string import Template

from time import sleep
import logging


class Chrome:
    driver = ""
    element = ""
    action_chains = ""
    url_list = []
    last_key = ""
    variables = {}
    errors = []

    def __init__(self, variables: dict):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | [%(name)s - %(levelname)s] | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger("Chrome")

        chrome_options = Options()
        # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--no-sandbox") #bypass OS security model
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('window-size=1920x1480')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"

        chrome_options.add_argument(f"user-agent={user_agent}")
        chrome_options.add_argument("headless")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.logger.info("Selenium initialized")
        self.driver.maximize_window()
        self.variables = variables

    def is_open(self, website):
        try:
            url = self.get_current_url()
            website = website.replace("https://", "")
            website = website.replace("http://", "")
            website = website.replace("www.", "")

            return website in url
        except:
            return False

    def open(self, website):
        if isinstance(self.driver, webdriver.Chrome):
            if not self.is_open(website):
                self.logger.info('Opening website: {}'.format(website))
                self.driver.get(website)
        else:
            self.logger.error("Driver instance not defined or misstyped")

    def get_element_and_add_actions(self, key_type: str, key: str, action: Action, step: str):
        try:
            if not self.element or self.last_key != key:
                self.logger.info(f"Searching for element with {key_type}={key}...")
                self.element: WebElement = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(locator=(key_type.lower(), key))
                )

            self.action_chains = Actions(self.driver)
            self.last_key = key
            self.logger.info(f"Element found: {self.element.tag_name}")
            if(self.element): 
                self.append_action(action)
            else: 
                self.errors.append(step)

        except NotImplementedError as error:
            self.logger.error(f"Fatal error in get_element_and_act: {error}")
            self.errors.append(step)

        except TimeoutException:
            self.logger.error(f"Cannot find element with {key_type}={key}")
            self.errors.append(step)


    def has_error_in_step(self, step: str):
        return step in self.errors

    def append_action(self, action: Action):
        action_type = action.get("type")
        action_params = action.get("params")
        action_value = action_params.get("value")
        
        try:
            if action_type == "click":
                self.action_chains.move_to_element(self.element)
                self.action_chains.click(on_element=self.element)
            elif action_type == "send_keys":
                send_keys_sentence = action_value
                if "$" in action_value:
                    variable_key = send_keys_sentence.replace("$", "")
                    variable_value = self.variables.get(variable_key)
                    send_keys_sentence = Utils.replace_variable_in_sentence(
                        sentence=send_keys_sentence, 
                        variable_key=variable_key, 
                        variable_value=variable_value
                    )

                self.logger.info(f"Sending keys: {send_keys_sentence}")
                self.action_chains.move_to_element(self.element)
                self.action_chains.send_keys(send_keys_sentence)
            elif action_type == "keyboard":
                action = Utils.get_function_from(Keys, action_params.get("value"))
                self.action_chains.move_to_element(self.element)
                self.action_chains.send_keys(action)
        except Exception as error:
            self.logger.exception(f"Fatal error in append_action: {error}")
            self.end_connection()

    def perform_actions(self):
        if type(self.action_chains) is Actions:
            self.action_chains.perform()

    def end_connection(self):
        # TODO: remove code below and implement it in correct way
        
        # list = self.driver.find_element(by=By.CLASS_NAME, value="s-main-slot")
        # item_names = list.find_elements(by=By.XPATH, value="//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-4']")
        # item_prices = list.find_elements(by=By.CLASS_NAME, value="a-price")
        # print('==========================')
        # print(f'names len: {len(item_names)}')
        # print(f'prices len: {len(item_prices)}')
        # for name in item_names:
        #     print (f"name: {name.text}")

        # for price in item_prices:
        #     print (f"price: {price.text}")
        # print('==========================')
        self.driver.close()
        self.driver.quit()

    def get_current_url(self):
        sleep(1)
        return self.driver.current_url

    def get_current_page_title(self):
        sleep(1)
        return self.driver.title
        