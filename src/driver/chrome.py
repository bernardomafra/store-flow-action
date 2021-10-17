from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Chrome:
    def __init__(self, headless):
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        if headless == True:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        print("initialized")

    def open(self, website):
        if isinstance(self.driver, webdriver.Chrome):
            self.driver.get(website)
        else:
            print("[Chrome.open]: error on driver instance")
