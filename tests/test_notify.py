import json

import pytest

from apps.notify import Notification

def test_config():
    with open('./config/config.json','r') as config_file:
        config = json.load(config_file)
        NOTIFICATION = config["NOTIFICATION"]
        token = NOTIFICATION["token"]
        channel = NOTIFICATION["channel"]
    assert ("xoxb-" in token) == True
    assert isinstance(channel, str) == True
    
def test_send_found_target_message():
    test_image = "static/test.png"
    #本当は画像ファイル作成時間を今の時間に置き換えたかった。
    #mocker.patch("apps.notification.Notification.create_time", return_value=datetime.now().replace(microsecond=0))
    #monkeypatch.setattr('apps.notify.Notification.send_found_target_message.create_time', datetime.now().replace(microsecond=0))
    notification = Notification()
    with pytest.raises(Exception):
        notification.send_found_target_message(test_image, "person")
    

def test_target_left_message():
    notification = Notification()
    response = notification.send_target_left_message("person", 10)
    assert response.status_code == 200