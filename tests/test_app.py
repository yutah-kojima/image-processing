import json

from apps.app import App

def test_config():
    with open('./config/config.json','r') as config_file:
        config = json.load(config_file)
        APP = config["APP"]
        weight_name = APP["weight_name"]
        weight_file = APP["weight_file"]
        set_timer = APP["set_timer"]
        camera_num = config["MAIN"]["camera_num"]
    assert ("yolox_" in weight_name) == True
    assert ("yolox_" and ".pth" in weight_file) == True
    assert isinstance(set_timer, int) == True
    assert isinstance(camera_num, int) == True 


def test_APP():
    
    with open('./config/config.json','r') as config_file:
        config = json.load(config_file)
        camera_num = config["MAIN"]["camera_num"]
    app_success = App(camera_num)
    assert app_success.cap.isOpened() == True


