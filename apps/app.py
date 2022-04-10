# coding: utf-8

import time
import copy
import torch
import importlib
from logging import getLogger

import cv2

from apps.notify import Notification
from apps.predictor import Predictor
from yolox.data.datasets import COCO_CLASSES

class App:
    def __init__(self, config):
        self.logger = getLogger(__name__)
        self.notification = Notification()
        # 設定
        APP = config["APP"]
        camera_num = APP["camera_num"]
        self.target_class = APP["target_class"]
        self.target_class_name = COCO_CLASSES[self.target_class]
        module_name = APP["module_name"]
        self.exp = importlib.import_module(module_name).Exp()
        self.weight_file = APP["weight_file"]
        self.set_timer = APP["set_timer"]
        self.allow_notification = APP["allow_notification"]  
        self.cap = cv2.VideoCapture(camera_num)
        if self.cap.isOpened() == False:
            self.logger.error('カメラにアクセス出来ません。')
            raise Error('カメラにアクセス出来ません。')
        self.logger.info('Success activate camera')
            
    def detect(self):
        # AIモデル構築とその中身の格納をして再現
        model = self.exp.get_model()
        model.eval()
        
        # 推論モデルの読み込み
        self.logger.info("loading checkpoint")
        checkpoint = torch.load(self.weight_file, map_location="cpu")
        model.load_state_dict(checkpoint["model"])
        self.logger.info("loaded checkpoint done.")
        
        predictor = Predictor(model, self.exp)
        
        staying_timer = 0
        found_target_first_time = True
        first_notification = False
        count_no_frame = 0
        while True:
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            if ret == False:
                count_no_frame += 1
                if count_no_frame == 3:
                    raise Error(self.logger.error('フレームが取得できません。'))
            else:
                result_frame = copy.deepcopy(frame)
                # 推論実施
                outputs, img_info = predictor.inference(frame)
                
                # デバック描画
                result_frame, detected_list = predictor.visual(outputs[0], img_info)
                # ターゲットがいる場合
                if self.target_class in detected_list:
                    # ターゲット初回発見時のログ
                    if found_target_first_time == True:
                        found_target_time = time.time()
                        self.logger.info('I found {}!!'.format(self.target_class_name))
                        found_target_first_time = False
                        first_notification = True
                    staying_timer = time.time() - found_target_time
                    self.logger.info('{} has been staying for {:.2f}s'.format(self.target_class_name, staying_timer))
                    # 滞留時間とターゲットの有無でSlackへ画像送信
                    if staying_timer >= self.set_timer and first_notification == True:
                        first_notification = False
                        self.logger.info('{} has stayed over {:.0f}s!'.format(self.target_class_name, staying_timer)) 
                        image = cv2.imwrite('./static/image.png', frame)
                        if self.allow_notification == True:
                            self.notification.send_found_target_message(image, self.target_class_name)
                # 推論結果がターゲット以外の場合
                else:
                    if first_notification == False:
                        self.logger.info('People left from here')
                        if self.allow_notification == True:
                            self.notification.send_target_left_message(self.target_class_name, staying_timer)
                    first_notification = True
                    staying_timer = 0
                    found_target_first_time = True

            # 画面反映
            cv2.imshow('frame', result_frame)
    
                    
            # [q]キーを入力されたら画面を閉じる
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # 終了処理
        self.cap.release()
        cv2.destroyAllWindows()
        self.logger.info('normal termination')
        
class Error(Exception):
    pass
    
    
