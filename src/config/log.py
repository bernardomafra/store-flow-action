import logging

def get_config():
    return logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | [%(name)s - %(levelname)s] | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
