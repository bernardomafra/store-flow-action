import os
from src.custom_types import Action

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from src.services.actions import Actions
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.keys import Keys

from src.utils import Utils

from time import sleep
import logging


class Chrome:
    driver = ""
    element = ""
    action_chains = ""
    url_list = []
    last_key = ""

    def __init__(self, headless):
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

        if headless == True:
            chrome_options.add_argument("headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.logger.info("Selenium initialized")
        self.driver.maximize_window()

    def is_open(self, website):
        try:
            url = self.driver.execute(Command.GET_CURRENT_URL).get("value")
            website = website.replace("https://", "")
            website = website.replace("http://", "")
            website = website.replace("www.", "")

            return website in url
        except:
            return False

    def open(self, website):
        self.logger.info('Opening website: {}'.format(website))
        if isinstance(self.driver, webdriver.Chrome):
            print(f"is ({website}) open? {self.is_open(website)}")
            if not self.is_open(website):
                self.driver.get(website)
        else:
            self.logger.error("Driver instance not defined or misstyped")

    def get_element_and_add_actions(self, key_type: str, key: str, action: Action):
        try:
            if not self.element or self.last_key != key:
                self.logger.info(f"Searching for element with {key_type}={key}...")
                self.element: WebElement = self.driver.find_element(
                    by=key_type.lower(), value=key
                )

            self.action_chains = Actions(self.driver)
            self.last_key = key
            self.logger.info(f"Element found: {self.element}")
            self.append_action(action)

        except NotImplementedError as error:
            self.logger.exception(f"Fatal error in get_element_and_act: {error}")

    def append_action(self, action: Action):
        action_type = action.get("type")
        action_params = action.get("params")
        
        try:
            if action_type == "click":
                self.action_chains.move_to_element(self.element)
                self.action_chains.click(on_element=self.element)
            elif action_type == "send_keys":
                self.action_chains.move_to_element(self.element)
                self.action_chains.send_keys(action_params.get("value"))
            elif action_type == "keyboard":
                action = Utils.get_function_from(Keys, action_params.get("value"))
                self.action_chains.move_to_element(self.element)
                self.action_chains.send_keys(action)
        except Exception as error:
            self.logger.exception(f"Fatal error in append_action: {error}")

    def perform_actions(self):
        self.action_chains.perform()