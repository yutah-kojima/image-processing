# -*- coding: utf-8 -*-

import json

import pytest

@pytest.fixture
def test_conf():
    CONF_PATH = './config/config.json'
    with open(CONF_PATH,'r') as config_file:
        config = json.load(config_file)
    return config

@pytest.fixture
def test_log_conf():
    LOG_CONF_PATH = './config/log_config.json'
    with open(LOG_CONF_PATH,'r') as log_config_file:
        log_config = json.load(log_config_file)
    return log_config

