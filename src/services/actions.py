import time
from typing import List
from selenium.webdriver import ActionChains


class Actions(ActionChains):
    def wait(self, time_s: float):
        self._actions.append(lambda: self.pause(time_s))
        return self

    def save_url(self, url_list: List, current_url: str):
        self._actions.append(lambda: url_list.append(current_url))
        return self
