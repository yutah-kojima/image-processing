# coding: utf-8

from apps.my_logger import get_logger
from apps.app import App

def main(config, log_config):
    logger = get_logger(log_config)
    logger.info('start')

    app = App(config)

    app.detect()   

if __name__ == "__main__":
    main()