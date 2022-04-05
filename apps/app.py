# coding: utf-8

from logging import getLogger
import cv2
import copy
import time
import importlib
import json

from apps.predictor import Predictor

from apps.notify import Notification

import torch

class App:
    def __init__(self, num = 0):
        self.logger = getLogger(__name__)
        self.notification = Notification()
        with open('./config/config.json','r') as config_file:
            config = json.load(config_file)
            APP = config["APP"]
            self.weight_name = APP["weight_name"]
            self.weight_file = APP["weight_file"]
            self.set_timer = APP["set_timer"]
            self.allow_notification = APP["allow_notification"]  


        self.cap = cv2.VideoCapture(num)
        if self.cap.isOpened() == False:
            self.logger.error('カメラにアクセス出来ません。')
            raise Error('カメラにアクセス出来ません。')
        self.logger.info('Success activate camera')
        
    def get_exp_by_name(self, exp_name):
        module_name = ".".join(["yolox", "exp", "default", exp_name])
        exp_object = importlib.import_module(module_name).Exp()
        return exp_object

    
    def detect(self, target = 0):
            
        exp = self.get_exp_by_name(self.weight_name)

        #この辺何やってるかわかりません。
        model = exp.get_model()
        model.eval()
        
        #推論モデルの読み込み？
        self.logger.info("loading checkpoint")
        checkpoint = torch.load(self.weight_file, map_location="cpu")
        model.load_state_dict(checkpoint["model"])
        self.logger.info("loaded checkpoint done.")
        
        predictor = Predictor(model, exp)
        
        start_time = time.time()
        staying_time = 0
        target_was_there = False
        while True:
            #Capture frame-by-frame
            #try文　いまいち使い方が分からない。
            try:
                ret, frame = self.cap.read()
            except Exception:
                raise Error(self.logger.error('フレームが取得できません。'))
            """
            #一応上記の元コード
            ret, frame = self.cap.read()
            if not ret:
                print("フレームが取得できません。")
                break
            """
            
            result_frame = copy.deepcopy(frame)
            # 推論実施
            outputs, img_info = predictor.inference(frame)
            
            detected_list = []
            #推論結果
            if outputs[0] != None:
                # デバッグ描画
                result_frame, detected_list = predictor.visual(outputs[0], img_info)
                
                for i in detected_list:
                    #ターゲットがいる場合、クラス取得＆滞留時間測定開始
                    if target in i:
                        target_class = i[1]
                        staying_time = time.time() - start_time
                        self.logger.info('{} has been staying for {:.2f}s'.format(target_class, staying_time))
                        #滞留時間とターゲットの有無でSlackへ画像送信
                        if staying_time >= self.set_timer and target_was_there == False:
                            target_was_there = True
                            self.logger.info('There is {}!'.format(target_class)) 
                            image = cv2.imwrite('./static/image.png', frame)
                            if self.allow_notification == True:
                                self.notification.send_found_target_message(image, target_class)
                    #ターゲット以外がいる場合
                    elif target in i == False:
                        if target_was_there == True:
                            self.logger.info('People left from here')
                            if self.allow_notification == True:
                                self.notification.send_target_left_message(target_class, staying_time)
                        staying_time = 0
                        start_time = time.time()
                        target_was_there = False
            #推論結果がない場合
            else:
                if target_was_there == True:
                    self.notification.send_target_left_message(target_class, staying_time)
                    self.logger.info('People left from here')
                staying_time = 0
                start_time = time.time()
                target_was_there = False

            # 画面反映
            cv2.imshow('frame', result_frame)
    
                    
            # [q]キーを入力されたら画面を閉じる
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        #終了処理
        self.cap.release()
        cv2.destroyAllWindows()
        self.logger.info('normal termination')
        
class Error(Exception):
    pass
    
    
