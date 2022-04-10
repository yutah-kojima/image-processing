#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (c) Megvii, Inc. and its affiliates.

import time
from logging import getLogger

import torch

from yolox.data.data_augment import ValTransform
from yolox.data.datasets import COCO_CLASSES
from yolox.utils import postprocess, vis


class Predictor(object):
    def __init__(
        self,
        model,
        exp,
        cls_names=COCO_CLASSES,
    ):
        self.model = model
        self.cls_names = cls_names
        self.num_classes = exp.num_classes
        self.nmsthre = exp.nmsthre
        self.test_size = exp.test_size
        self.preproc = ValTransform(legacy=False)
        
        #ログ
        self.logger = getLogger(__name__)

    def inference(self, img):
        
        img_info = {"id": 0}
        img_info["raw_img"] = img

        ratio = min(self.test_size[0] / img.shape[0], self.test_size[1] / img.shape[1])
        img_info["ratio"] = ratio

        img, _ = self.preproc(img, None, self.test_size)
        img = torch.from_numpy(img).unsqueeze(0)
        img = img.float()

        with torch.no_grad():
            t0 = time.time()
            outputs = self.model(img)
            #画像処理
            outputs = postprocess(outputs, self.num_classes, self.nmsthre, class_agnostic=True)
            #推論時間ログ
            self.logger.info(f"Infer time: {(time.time() - t0):.4f}s")
        return outputs, img_info

    def visual(self, output, img_info, cls_conf=0.35):
        ratio = img_info["ratio"]
        img = img_info["raw_img"]
        detected_list = []
        if output is None:
            return img, detected_list
        output = output.cpu()
        bboxes = output[:, 0:4]
        # preprocessing: resize
        bboxes /= ratio
        cls = output[:, 6]
        for i in range(len(cls)):
            class_id = int(cls[i])
            detected_list.append(class_id)
        scores = output[:, 4] * output[:, 5]
        vis_res = vis(img, bboxes, scores, cls, cls_conf, self.cls_names)
        return vis_res, detected_list