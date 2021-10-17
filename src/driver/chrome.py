from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging


class Chrome:
    def __init__(self, headless):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | [%(name)s - %(levelname)s] | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger("Chrome")

        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        if headless == True:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.logger.info(f"Selenium initialized")

    def open(self, website):
        if isinstance(self.driver, webdriver.Chrome):
            self.driver.get(website)
        else:
            self.logger.error(f"Driver instance not defined or misstyped")
