# coding: utf-8

from apps.my_logger import get_logger
from apps.app import App
import json

def main():
    with open('./config/config.json','r') as config_file:
        config = json.load(config_file)
        MAIN = config["MAIN"]
        camera_num = MAIN["camera_num"]
        target_class = MAIN["target_class"]

        logger = get_logger()
        logger.info('start')

        app = App(camera_num)

        app.detect(target_class)   

if __name__ == "__main__":
    main()