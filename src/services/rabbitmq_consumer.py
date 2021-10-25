import logging

from typing import NewType

FlowData = NewType("FlowData", dict(key_type=str, key=str, step=str, action=str))

# ID
# XPATH
# LINK_TEXT
# PARTIAL_LINK_TEXT
# NAME
# TAG_NAME
# CLASS_NAME
# CSS_SELECTOR


class RabbitMQConsumer:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | [%(name)s - %(levelname)s] | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    data = {
        "id": "1234",
        "search": "Some product",
        "finished": False,
        "actions": {
            "https://magazineluiza.com.br": {
                "flow": [
                    {
                        "key_type": "ID",
                        "key": "input-search",
                        "step": "search",
                        "action": {"type": "click", "params": {}},
                    },
                    {
                        "key_type": "ID",
                        "key": "input-search",
                        "step": "search",
                        "action": {
                            "type": "send_keys",
                            "params": {"value": "Macbook Air"},
                        },
                    },
                    {
                        "key_type": "ID",
                        "key": "input-search",
                        "step": "search",
                        "action": {
                            "type": "keyboard",
                            "params": {"value": "ENTER"},
                        },
                    },
                ]
            },
            "https://casasbahia.com.br": {
                "flow": [
                    {
                        "key_type": "ID",
                        "key": "strBusca",
                        "step": "search",
                        "action": {"type": "click", "params": {}},
                    },
                    {
                        "key_type": "ID",
                        "key": "strBusca",
                        "step": "search",
                        "action": {
                            "type": "send_keys",
                            "params": {"value": "Macbook Air"},
                        },
                    },
                    {
                        "key_type": "ID",
                        "key": "strBusca",
                        "step": "search",
                        "action": {
                            "type": "keyboard",
                            "params": {"value": "ENTER"},
                        },
                    },
                ]
            },
            "https://fastshop.com.br": {
                "flow": [
                    {
                        "key_type": "ID",
                        "key": "search-box-id",
                        "step": "search",
                        "action": {"type": "click", "params": {}},
                    },
                    {
                        "key_type": "ID",
                        "key": "search-box-id",
                        "step": "search",
                        "action": {
                            "type": "send_keys",
                            "params": {"value": "Macbook Air"},
                        },
                    },
                    {
                        "key_type": "ID",
                        "key": "search-box-id",
                        "step": "search",
                        "action": {
                            "type": "keyboard",
                            "params": {"value": "ENTER"},
                        },
                    },
                ]
            },
        },
    }

    def get(self):
        return self.data
