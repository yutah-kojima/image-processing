# coding: utf-8

from apps.app import App


def test_check_config(test_conf):
    APP = test_conf["APP"]
    camera_num = APP["camera_num"]
    target_class = APP["target_class"]
    module_name = APP["module_name"]
    weight_file = APP["weight_file"]
    set_timer = APP["set_timer"]
    allow_notification = APP["allow_notification"]
    assert isinstance(camera_num, int) == True
    assert 0 <= target_class <= 79
    assert ("yolox.exp.default.yolox_" in module_name) == True
    assert ("YOLOX/weights/yolox_" and ".pth" in weight_file) == True
    assert isinstance(set_timer, int) == True
    assert isinstance(allow_notification, bool) == True

def test_check_camera(test_conf):
    app_success = App(test_conf)
    assert app_success.cap.isOpened() == True


