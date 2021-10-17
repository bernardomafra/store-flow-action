from driver.chrome import Chrome
from messaging.rabbitmq import RabbitMQ

browser = Chrome(headless=True)
queue = RabbitMQ(host="localhost", port=5672)


def open_website(website):
    browser.open(website)
    queue.send_message(f"Website openned {website}")


open_website("https://google.com.br")
