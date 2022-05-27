import os
import re
import time
from random import randint
from src.custom_types import Action

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from src.services.actions import Actions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select

from src.utils import Utils
from string import Template

import time 
import logging


class Chrome:
    driver = ""
    element = ""
    action_chains = ""
    url_list = []
    last_key = ""
    variables = {}
    errors = []
    skip_conditions = []

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
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('window-size=1920x1480')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"

        chrome_options.add_argument(f"user-agent={user_agent}")
        # chrome_options.add_argument("headless")

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
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
            if "$" in key:
                # variable_key = re.findall(r"\$\w+", "//button[@aria-label='$size' i]")[0].replace("$", "")
                variable_key = re.findall(r"\$\w+", key)[0].replace("$", "")
                variable_value = self.variables.get(variable_key)
                key = Utils.replace_variable_in_sentence(
                    sentence=key, 
                    variable_key=variable_key, 
                    variable_value=variable_value
                )

            if key_type == 'SCREENSHOT':
                # save screenshot with today`s date and time as in a clients folder
                client_name = self.variables.get('name') or 'unknown'
                self.driver.save_screenshot(f"{client_name.split(' ')[0]}-{time.strftime('%Y-%m-%d')}-{time.strftime('%H-%M-%S')}-{key}.png")
                return
            elif not self.element or self.last_key != key:
                self.logger.info(f"Searching for element with {key_type}={key}...")
                self.element: WebElement = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(locator=(key_type.lower(), key))
                )
                self.logger.info(f"Element found: {self.element.tag_name}")

            self.action_chains = Actions(self.driver)
            self.last_key = key
            if(self.element): 
                self.append_action(action)
            else: 
                self.errors.append(step)

        except NotImplementedError as error:
            self.logger.error(f"Fatal error in get_element_and_act: {error}")
            self.errors.append(step)

        except TimeoutException:
            if step == 'verificando se existe endereço cadastrado':
                return
            self.logger.error(f"Cannot find element with {key_type}={key}")
            if not action.get('type') == 'conditional':
                self.errors.append(step)
        
        except Exception as error:
            self.logger.error(f"Fatal error in get_element_and_act: {error}")
            self.errors.append(step)


    def has_error_in_step(self, step: str):
        return step in self.errors

    def append_action(self, action: Action):
        action_type = action.get("type")
        action_params = action.get("params")
        action_value = action_params.get("value")
        self.driver.implicitly_wait(10) # seconds

        try:
            if action_value and "$" in action_value:
                variable_key = action_value.replace("$", "")
                variable_value = self.variables.get(variable_key)
                action_value = Utils.replace_variable_in_sentence(
                    sentence=action_value, 
                    variable_key=variable_key, 
                    variable_value=variable_value
                )

            if action_params.get('register_skip_condition'):
                self.skip_conditions.append(action_params.get('register_skip_condition'))

            if action_type == "click":
                self.action_chains.move_to_element(self.element)
                self.action_chains.click(on_element=self.element)
                time.sleep(2) 
            elif action_type == "select":
                select_object = Select(self.element)
                if action_params.get('by') != None and action_params.get('by') == "visible_text":
                    select_object.select_by_visible_text(action_value)
                else: 
                    select_object.select_by_value(action_value)
            elif action_type == "send_keys":
                self.logger.info(f"Sending keys: {action_value}")
                self.action_chains.move_to_element(self.element)
                self.action_chains.click(on_element=self.element)
                if action_value != self.element.text and action_params.get('override') != 'bypass':
                    self.action_chains.send_keys(action_value)
            elif action_type == "keyboard":
                action = Utils.get_function_from(Keys, action_params.get("value"))
                self.action_chains.move_to_element(self.element)
                self.action_chains.send_keys(action)
            elif action_type == "hover":
                self.action_chains.move_to_element(self.element)
            elif action_type == "continue":
                self.logger.info(f"Continuing with next step")

        except ElementNotInteractableException as not_interactable_err:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", self.element);
            self.action_chains.click(on_element=self.element)
        except Exception as error:
            self.logger.exception(f"Fatal error in append_action: {error}")
            self.end_connection()

    def perform_actions(self):
        if type(self.action_chains) is Actions:
            self.action_chains.perform()

    def end_connection(self):
        self.skip_conditions = []
        self.errors = []
        self.driver.close()
        self.driver.quit()

    def get_current_url(self):
        time.sleep(1)
        return self.driver.current_url

    def get_current_page_title(self):
        time.sleep(1)
        return self.driver.title
        