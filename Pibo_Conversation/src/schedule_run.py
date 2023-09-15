import os, sys, subprocess
import numpy as np
import pandas as pd
import random
import csv
import time
from datetime import datetime

sys.path.append('/home/pi')
from schedule_update import UpdateSchedule
from Pibo_Package_02.Pibo_Conversation.data.text_to_speech import TextToSpeech, text_to_speech
from Pibo_Package_02.Pibo_Conversation.src.drive_upload import drive_upload

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
        

        ## 고정된 스케줄로 진행(~3일차)
                
        # 최초 실행시 자기소개 시나리오 실행
        if self.completion == 12: 
            self.act = f'Pibo_Conversation/src/greeting.py'
        
        if 13 <= self.completion <= 20:
            fix = {13:'Pibo_Conversation/src/Fairytale/19_shepherd.py', 14:'Pibo_Conversation/src/Roleplay/02_strong.py',
                   15:'Pibo_Conversation/src/Solution/01_badword.py', 16:'Pibo_Play/src/Com/com_4.py', 17:'Pibo_Play/src/Soc/soc_6.py',
                   18:'Pibo_Conversation/src/Etiquette/03_cough.py', 19:'Pibo_Play/src/Cog/cog_1.py', 20:'Pibo_Play/src/Mus/mus_11.py'}   
            self.act = fix.get(self.completion)
            
        
        ## 선호도 계산해서 활동 스케줄 결정(4일차~)
        
        if 21 <= self.completion <= 22 or self.completion >= 24:
            for i in range(0, len(data2)):
                for j in range(0, 4):
                    data2[i][j] = float(data2[i][j])    # 점수 값이 string 형태로 들어있어서 flaot로 변환
            print(data2)

            for i in range(0, len(data2)-1):            # 각 항목끼리 모두 합연산
                data3 = [sum(i) for i in zip(*data2)]   # data1 목록 만큼
            print("선호도 총합:", data3)   
            
            result = us.update(new_preference=data3)[0]    
                    
            
            if result == '사회성':            
                # 완료한 활동 개수가 짝수면 놀이, 홀수면 대화
                if self.completion % 2 == 0: 
                    # rand = random.choice([2, 3])
                    self.act = f'Pibo_Play/src/Soc/soc_2.py'
                
                if self.completion % 2 != 0:
                    # rand = random.choice(['06_street', '14_giveaway'])
                    self.act = f'Pibo_Conversation/src/Etiquette/14_giveaway.py'
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
        
        # 마지막 활동은 헤어짐 시나리오 실행 
        if self.completion == 23:
            self.act = f'Pibo_Conversation/src/goodbye.py'           
        
        try:
            folder = "/home/pi/UserData"
            logfile = f'(P02)_{datetime.now().strftime("%m%d_%H%M")}.txt'   #('P<PACKAGE_NUMBER>_DATE.txt')   
            f = open(f'{folder}/{logfile}','w')
            
            # os.system(f'python3 {self.path}/{self.act}')
            out = subprocess.check_output([f'python3 {self.path}/{self.act}'], shell=True, stderr=subprocess.STDOUT, encoding="utf-8")  
            
            f.write(out)
            f.close()            
            
            try:
                drive_upload(filepath=f'{folder}/{logfile}', filename=logfile)
                
            except Exception as e:
                print(e)
            
            # 더 하고 싶다고 하면 여기서부터
            if self.completion >= 24:
                pass
            
            else:
                text_to_speech(text="파이보랑 또 놀자!")            
                motion.set_motion("m_wakeup", 1)
                subprocess.run(['python3 /home/pi/Pibo_Package_02/Pibo_Conversation/src/start_touch.py'], shell=True)
            # 여기까지 주석!! 대신 다음 활동 하려면 매번 재부팅 해야함
            
        except Exception as ex:
            with open('/home/pi/pibo_errmsg', 'w') as f:
                f.write(f'[{time.ctime()}]\n{ex}')
                
        
        



if __name__ == '__main__':
    
    # pibo_audio.mute(True)
    
    rs = RunSchedule()
    rs.day()
