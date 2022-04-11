# -*- coding: utf-8 -*-

import pytest

from apps.notify import Notification

def test_config(test_conf):
    NOTIFICATION = test_conf["NOTIFICATION"]
    token = NOTIFICATION["token"]
    channel = NOTIFICATION["channel"]
    assert ("xoxb-" in token) == True
    assert isinstance(channel, str) == True
    
def test_send_found_target_message(test_conf):
    path_test_img_file = "static/test.png"
    #本当は画像ファイル作成時間を今の時間に置き換えたかった。
    #mocker.patch("apps.notification.Notification.create_time", return_value=datetime.now().replace(microsecond=0))
    #monkeypatch.setattr('apps.notify.Notification.send_found_target_message.create_time', datetime.now().replace(microsecond=0))
    notification = Notification(test_conf)
    with pytest.raises(Exception):
        notification.send_found_target_message(path_test_img_file, "person")
    

def test_target_left_message(test_conf):
    notification = Notification(test_conf)
    try:
        response = notification.send_target_left_message("person", 10)
    except Exception as e:
        raise Exception('config.jsonのSlack tokenもしくはchannelが間違っています。')
    else:
        assert response.status_code == 200
    