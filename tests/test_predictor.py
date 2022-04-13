# coding: utf-8

import cv2
import torch
import numpy
import pytest
import importlib

from apps.app import App
from apps.predictor import Predictor

@pytest.fixture
def test_predictor(test_conf):
    APP = test_conf["APP"]
    module_name = APP["module_name"]
    weight_file = APP["weight_file"]

    #app = App(test_conf)
    exp = importlib.import_module(module_name).Exp()
    model = exp.get_model()
    model.eval()
    checkpoint = torch.load(weight_file, map_location="cpu")
    model.load_state_dict(checkpoint["model"])

    predictor = Predictor(model, exp)
    return predictor

@pytest.fixture
def test_img_dog():
    PATH_IMG = 'YOLOX/assets/dog.jpg'
    test_img_dog = cv2.imread(PATH_IMG)
    return test_img_dog

@pytest.fixture
def test_blank_img():
    PATH_BLANK_IMG = 'static/test_blank_img.png'
    test_blank_img = cv2.imread(PATH_BLANK_IMG)
    return test_blank_img


def test_inferance(test_predictor, test_img_dog):
    outputs, img_info = test_predictor.inference(test_img_dog)
    assert isinstance(outputs,list) == True
    assert ('id' in img_info) == True
    

def test_visual_something(test_predictor, test_img_dog):
    outputs, img_info = test_predictor.inference(test_img_dog)
    result_frame, detected_list = test_predictor.visual(outputs[0], img_info)
    assert type(result_frame) == numpy.ndarray 
    assert type(detected_list) == list
    
def test_visual_nothing(test_predictor, test_blank_img):
    outputs, img_info = test_predictor.inference(test_blank_img)
    assert outputs[0] == None
    result_frame, detected_list = test_predictor.visual(outputs[0], img_info)
    assert type(result_frame) == numpy.ndarray 
    assert detected_list == []
