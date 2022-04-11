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
def test_img():
    PATH_IMG = 'YOLOX/assets/dog.jpg'
    test_img = cv2.imread(PATH_IMG)
    return test_img


def test_inferance(test_predictor, test_img):
    outputs, img_info = test_predictor.inference(test_img)
    assert isinstance(outputs,list) == True
    assert ('id' in img_info) == True
    

def test_visual(test_predictor, test_img):
    outputs, img_info = test_predictor.inference(test_img)
    result_frame, detected_list = test_predictor.visual(outputs[0], img_info)
    assert type(result_frame) == numpy.ndarray 
    assert type(detected_list) == list