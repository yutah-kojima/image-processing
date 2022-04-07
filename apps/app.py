# coding: utf-8

import time
import copy
import torch
import importlib
from logging import getLogger

import cv2

from apps.notify import Notification
from apps.predictor import Predictor


class App:
    def __init__(self, config):
        self.logger = getLogger(__name__)
        self.notification = Notification()
        # 設定
        APP = config["APP"]
        camera_num = APP["camera_num"]
        self.target_class = APP["target_class"]
        module_name = APP["weight_name"]
        self.exp = importlib.import_module(module_name).Exp()
        self.weight_file = APP["weight_file"]
        self.set_timer = APP["set_timer"]
        self.allow_notification = APP["allow_notification"]  
        self.cap = cv2.VideoCapture(camera_num)
        if self.cap.isOpened() == False:
            self.logger.error('カメラにアクセス出来ません。')
            raise Error('カメラにアクセス出来ません。')
        self.logger.info('Success activate camera')
        
    """   
    def get_exp_by_name(self, exp_name):
        module_name = ".".join(["yolox", "exp", "default", exp_name])
        exp_object = importlib.import_module(module_name).Exp()
        return exp_object
    """
    
    def detect(self):
            
        # exp = self.get_exp_by_name(self.weight_name)
        
        
        # この辺何やってるかわかりません。
        model = self.exp.get_model()
        model.eval()
        
        # 推論モデルの読み込み？
        self.logger.info("loading checkpoint")
        checkpoint = torch.load(self.weight_file, map_location="cpu")
        model.load_state_dict(checkpoint["model"])
        self.logger.info("loaded checkpoint done.")
        
        predictor = Predictor(model, self.exp)
        
        start_time = time.time()
        staying_time = 0
        target_was_there = False
        count_no_frame = 0
        while True:
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            if frame == None:
                count_no_frame += 1
                if count_no_frame == 3:
                    raise Error(self.logger.error('フレームが取得できません。'))
            """
            # 一応上記の元コード
            ret, frame = self.cap.read()
            if not ret:
                print("フレームが取得できません。")
                break
            """
            
            result_frame = copy.deepcopy(frame)
            # 推論実施
            outputs, img_info = predictor.inference(frame)
            
            detected_list = []
            # 推論結果
            if outputs[0] != None:
                # デバッグ描画
                result_frame, detected_list = predictor.visual(outputs[0], img_info)
                
                for i in detected_list:
                    # ターゲットがいる場合、クラス取得＆滞留時間測定開始
                    if self.target_class in i:
                        target_class_name = i[1]
                        staying_time = time.time() - start_time
                        self.logger.info('{} has been staying for {:.2f}s'.format(target_class_name, staying_time))
                        # 滞留時間とターゲットの有無でSlackへ画像送信
                        if staying_time >= self.set_timer and target_was_there == False:
                            target_was_there = True
                            self.logger.info('There is {}!'.format(target_class_name)) 
                            image = cv2.imwrite('./static/image.png', frame)
                            if self.allow_notification == True:
                                self.notification.send_found_target_message(image, target_class_name)
                    # ターゲット以外がいる場合
                    elif self.target_class in i == False:
                        if target_was_there == True:
                            self.logger.info('People left from here')
                            if self.allow_notification == True:
                                self.notification.send_target_left_message(target_class_name, staying_time)
                        staying_time = 0
                        start_time = time.time()
                        target_was_there = False
            # 推論結果がない場合
            else:
                if target_was_there == True:
                    self.notification.send_target_left_message(target_class_name, staying_time)
                    self.logger.info('People left from here')
                staying_time = 0
                start_time = time.time()
                target_was_there = False

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
    
    
