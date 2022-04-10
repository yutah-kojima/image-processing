# -*- coding: utf-8 -*-

from slack_sdk import WebClient
import os
from datetime import datetime
import time
from logging import getLogger

class Notification:
    def __init__(self, config):
        self.logger = getLogger(__name__)
        NOTIFICATION = config["NOTIFICATION"]
        token = NOTIFICATION["token"]
        self.channel = NOTIFICATION["channel"]
        self.client = WebClient(token)
        
    def send_found_target_message(self, target, PATH_IMG):

        message = "{}がいます。".format(target)      
                
        #ファイルの作成日
        while True:
            create_time = datetime.fromtimestamp(int(os.path.getctime(PATH_IMG)))
            time_difference = (datetime.now().replace(microsecond=0) - create_time)
            if time_difference.seconds <= 10:
                r = self.client.files_upload(channels = self.channel, file = PATH_IMG, initial_comment= message, filename="target")
                break
            elif time_difference.seconds > 20:
                self.logger.error('画像が保存できていません。')
                raise Exception()
            else:
                time.sleep(1)
        self.logger.info('Success sending message & image')
        return r
    
    def send_target_left_message(self, target, staying_time):
        message = '{}は{:.0f}秒間居ました。'.format(target, staying_time)
        r = self.client.chat_postMessage(channel=self.channel, text=message)
        self.logger.info('Success sending message')
        return r