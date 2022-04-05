# -*- coding:utf-8 -*-
import json
from logging import getLogger, config


def get_logger():
    """ 設定ファイルの読み込む """
    with open('config/log_config.json', 'r', encoding='utf-8') as config_file:
        log_conf = json.load(config_file)
        config.dictConfig(log_conf)
    
    # root loggerを取得
    logger = getLogger(__name__)
    
    return logger