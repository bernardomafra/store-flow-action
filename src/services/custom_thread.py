import threading


class CustomThread(threading.Thread):
    def __init__(self, idt, name):
        threading.Thread.__init__(self)
        self.idt = idt
        self.name = name

    def run(self, func):
        print(f"Iniciando a thread {self.name}")
        func()
        print(f"Fim da thread {self.name}")
