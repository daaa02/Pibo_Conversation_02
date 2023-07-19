import os, sys, subprocess
import numpy as np
import pandas as pd
import random
import csv
import time
from datetime import datetime

sys.path.append('/home/pi')
from schedule_update import UpdateSchedule
from Pibo_Conversation.data.text_to_speech import TextToSpeech, text_to_speech

from openpibo.audio import Audio
from openpibo.motion import Motion
from openpibo.oled import Oled

us = UpdateSchedule()
pibo_audio = Audio()
motion = Motion()
oled = Oled()


class RunSchedule():
    
    def __init__(self):
        self.path = '/home/pi/Pibo_Package_02'
        self.completion = int
        self.act = ''


    def day(self):
        UDfolder = "/home/pi/UserData"
        file = open(f"{UDfolder}/aa.csv", 'r', newline='', encoding='latin-1')
        cr = csv.reader((row.replace('\0', '').replace('\x00', '') for row in file),
                        delimiter=',', doublequote=True, lineterminator='\r\n', quotechar='"')
        # cr = csv.reader(file, delimiter=',', doublequote=True, lineterminator='\r\n', quotechar='"')
        
        data1 = []
        data2 = []
        data3 = []
        
        for row in cr:
            # print(row[2:])      
            data1.append(row[2:])                       # 모든 행의 세 번째 열부터 취급
            
        data2 = data1[1:]
        # print(data2)                                  # [점수], [점수], ...
        self.completion = len(data2)
        print('완료한 활동 개수:', self.completion)

        # 고정된 스케줄로 진행(~3일차)
        if self.completion < 8:
            # 완료한 활동 개수가 짝수면 놀이, 홀수면 대화
            # fix = {0:'Pibo_Play/src/Mus/mus_11.py', 1:'Pibo_Conversation/src/Roleplay/02_strong.py',#'Pibo_Conversation/src/Roleplay/09_rolemodel.py', 
            #        2:'Pibo_Play/src/Cog/cog_1.py', 3:'Pibo_Conversation/src/Fairytale/04_wolf.py', 
            #        4:'Pibo_Play/src/Soc/soc_6.py', 5:'Pibo_Conversation/src/Etiquette/03_cough.py', 
            #        6:'Pibo_Play/src/Com/com_4.py', 7:'Pibo_Conversation/src/Solution/01_badword.py'}            
            fix = {0:'Pibo_Conversation/src/Fairytale/19_shepherd.py', 1:'Pibo_Conversation/src/Roleplay/02_strong.py',
                   2:'Pibo_Conversation/src/Solution/01_badword.py', 3:'Pibo_Play/src/Com/com_4.py', 4:'Pibo_Play/src/Soc/soc_6.py',
                   5:'Pibo_Conversation/src/Etiquette/03_cough.py', 6:'Pibo_Play/src/Cog/cog_1.py', 7:'Pibo_Play/src/Mus/mus_11.py'}   
            self.act = fix.get(self.completion)
        
        # 선호도 계산해서 활동 스케줄 결정(4일차~)
        if self.completion >= 8:
            for i in range(0, len(data2)):              # 점수 값이 string 형태로 들어있어서 flaot로 변환
                for j in range(0, 4):
                    data2[i][j] = float(data2[i][j])
            print(data2)

            for i in range(0, len(data2)-1):            # 각 항목끼리 모두 합연산
                data3 = [sum(i) for i in zip(*data2)]   # data1 목록 만큼
            print("선호도 총합:", data3)   
            
            result = us.update(new_preference=data3)[0]
            
            
            if result == '사회성':            
                # 완료한 활동 개수가 짝수면 놀이, 홀수면 대화
                if self.completion % 2 == 0: 
                    rand = random.choice([2, 3])
                    self.act = f'Pibo_Play/src/Soc/soc_{rand}.py'
                
                if self.completion % 2 != 0:
                    rand = random.choice(['06_street', '14_giveaway'])
                    self.act = f'Pibo_Conversation/src/Etiquette/{rand}.py'
                    # self.act = f'Pibo_Conversation/src/Etiquette/00_qrcode.py'
                
            if result == '의사소통':
                # 완료한 활동 개수가 짝수면 놀이, 홀수면 대화
                if self.completion % 2 == 0: 
                    rand = random.choice([1, 2])
                    self.act = f'Pibo_Play/src/Com/com_{rand}.py'
                
                if self.completion % 2 != 0:
                    rand = random.choice(['02_salt', '18_rabbit'])
                    self.act = f'Pibo_Conversation/src/Fairytale/{rand}.py'
                
            if result == '인지':
                # 완료한 활동 개수가 짝수면 놀이, 홀수면 대화
                if self.completion % 2 == 0: 
                    rand = random.choice([3, 10])
                    self.act = f'Pibo_Play/src/Cog/cog_{rand}.py'
                
                if self.completion % 2 != 0:
                    rand = random.choice(['02_wash', '03_night', '17_thank', '18_cheerup'])
                    self.act = f'Pibo_Conversation/src/Solution/{rand}.py'
                
            if result == '근육':
                # 완료한 활동 개수가 짝수면 놀이, 홀수면 대화
                if self.completion % 2 == 0:
                    rand = random.choice([1, 8, 12])
                    self.act = f'Pibo_Play/src/Mus/mus_{rand}.py'
                    
                if self.completion % 2 != 0:
                    rand = random.choice(['03_tiny', '04_flying'])
                    self.act = f'Pibo_Conversation/src/Roleplay/{rand}.py'
        
        # 마지막 활동은 헤어짐 시나리오: 얘 끝나고 밑에 다음에 ~ 안나오게 해야함
        if self.completion == 10:
            self.act = f'Pibo_Conversation/src/goodbye.py'           
        
        folder = "/home/pi/UserData"
        today = datetime.now().strftime('%y%m%d_%H%M')
        # f = open(f'{folder}/{today}.txt','w')        
        # out = subprocess.check_output([f'python3 /home/pi/Pibo_Package_02/Pibo_Conversation/src/greeting.py'], shell=True, stderr=subprocess.STDOUT, encoding="utf-8")  
        
        try:
            # out = subprocess.run([f'python3 {self.path}/{self.act}'], shell=True)
            # subprocess.run([f'python3 {self.path}/{self.act}'], shell=True)
            os.system(f'python3 {self.path}/{self.act}')
            
            if self.completion >= 10:
                pass
            
            else:
                text_to_speech(text="파이보랑 또 놀자!")            
                motion.set_motion("m_wakeup", 1)
                subprocess.run(['python3 /home/pi/Pibo_Package_02/Pibo_Conversation/src/start_touch.py'], shell=True)
            
            
            # # 완료한 활동 개수가 짝수면 종료, 홀수면 계속
            # if self.completion % 2 == 0:
            #     text_to_speech(text="다음에 또 놀자!")
            #     # text_to_speech(text="오늘 활동이 끝났어! 내일 또 만나자 안녕~!")
            #     motion.set_motion("m_wakeup", 1)
            #     subprocess.run(['python3 /home/pi/Pibo_Package_02/Pibo_Conversation/src/start_touch.py'], shell=True)
                
            # if self.completion % 2 != 0:
            #     text_to_speech(text="다음 활동을 하고 싶으면 또 머리를 쓰다듬어줘!")
            #     motion.set_motion("m_wakeup", 1)                
            #     subprocess.run(['python3 /home/pi/Pibo_Package_02/Pibo_Conversation/src/start_touch.py'], shell=True)
        
        except Exception as ex:
            with open('/home/pi/pibo_errmsg', 'w') as f:
                f.write(f'[{time.ctime()}]\n{ex}')
                
        
        



if __name__ == '__main__':
    
    # pibo_audio.mute(True)
    
    rs = RunSchedule()
    rs.day()