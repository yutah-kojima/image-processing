#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from apps import main

PATH_CONFIG = './config/config.json'
PATH_LOG_CONFIG = './config/log_config.json'
with open(PATH_CONFIG,'r') as config_file:
    config = json.load(config_file)
with open(PATH_LOG_CONFIG, 'r') as log_config_file:
    log_config = json.load(log_config_file)

# python run.pyで実行
if __name__ == "__main__":
    main.main(config, log_config)

