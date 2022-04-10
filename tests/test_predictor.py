# coding: utf-8

import json

import cv2
import torch
import numpy

from apps.app import App
from apps.predictor import Predictor

with open('./config/config.json','r') as config_file:
    config = json.load(config_file)
    APP = config["APP"]
    weight_name = APP["weight_name"]
    weight_file = APP["weight_file"]

app = App()
exp = app.get_exp_by_name(weight_name)
model = exp.get_model()
model.eval()
checkpoint = torch.load(weight_file, map_location="cpu")
model.load_state_dict(checkpoint["model"])

predictor = Predictor(model, exp)
img = cv2.imread('YOLOX/assets/dog.jpg')


def test_inferance():
    outputs, img_info = predictor.inference(img)
    assert isinstance(outputs,list) == True
    assert ('id' in img_info) == True
    

def test_visual():
    outputs, img_info = predictor.inference(img)
    result_frame, detected_list = predictor.visual(outputs[0], img_info)
    assert type(result_frame) == numpy.ndarray 
    assert type(detected_list) == list