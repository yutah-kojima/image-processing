# -*- coding:utf-8 -*-

from logging import getLogger, config


def get_logger(log_config):
    config.dictConfig(log_config)
    
    # root loggerを取得
    logger = getLogger(__name__)
    
    return logger