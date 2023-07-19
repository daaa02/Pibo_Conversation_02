# -*- coding: utf-8 -*-

# 사회기술-함께 있는 공간에서 소리 내어 음식을 먹지 않아요

import os, sys
import re
import csv
import random
from datetime import datetime
import time
import json

# sys.path.append('/home/kiro/workspace/Conversation_Scenarios/')

sys.path.append('/home/pi/Pibo_Package_02/Pibo_Play/')
from data.p_conversation_manage import ConversationManage, WordManage, NLP
from data.speech_to_text import speech_to_text
from data.text_to_speech import TextToSpeech, text_to_speech
import data.behavior.behavior_list as behavior
from data.spread import google_spread_sheet

cm = ConversationManage()
wm = WordManage()
nlp = NLP()
audio = TextToSpeech()
gss = google_spread_sheet()

folder = "/home/pi/UserData"
filename = os.path.basename(__file__).strip('.py')
today = datetime.now().strftime('%m%d_%H%M')
csv_conversation = open(f'{folder}/{today}_{filename}.csv', 'a', newline='', encoding = 'utf-8')
csv_preference = open(f'{folder}/aa.csv', 'a', newline='', encoding = 'utf-8')
cwc = csv.writer(csv_conversation)
cwp = csv.writer(csv_preference)
crc = csv.reader(csv_conversation, delimiter=',', doublequote=True, lineterminator='\r\n', quotechar='"')


class Com():
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = config['user_name'] 
        self.aa = ''
        self.score = []
        self.turns = []
        self.reject = []
        
        self.Positive = ['pos', '좋아', '좋은', '좋았', '좋다', '재미있', '재미 있', '재밌', '재밌어']
        self.Negative = ['neg', '별로', '아니', '안 해', '안해', '안 할래', '안 하', '싫어', '싫', '재미없', '재미 없']
        self.Neutral = ['neu', '글쎄', '몰라', '모르', '몰라', '몰랐', '보통']  
        
        
    def com_4(self):
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"춤추는 유령 놀이를 해보자!")
        time.sleep(1)        
        pibo = cm.tts(bhv="do_explain_A", string=f"이번 놀이는 준비물이 필요없어! 놀이 방법을 알려줄께!")
        time.sleep(1) 
        pibo = cm.tts(bhv="do_suggestion_S", string=f"음악이 나오면 주문을 외치고 마음껏 춤을 추면 돼. 주문을 따라해보자!")
        time.sleep(1)
        pibo = cm.tts(bhv="do_joy_A", string=f"‘우리는 춤을 추는 유령이에요’. 한번 따라해 보자!")
        cwc.writerow(['pibo', pibo])
        
        while True:
            answer = cm.responses_proc(re_q="do_suggestion_S", re_bhv="한번 따라해봐! 우리는 춤을 추는 유령이에요~")
            
            pibo = cm.tts(bhv="do_explain_B", string=f"좋았어! 만약에 음악이 멈추면 제자리에서 정지해야 돼. 그리고 다시 음악이 나올 때 다시 춤을 추면 돼.")
            cwc.writerow(['pibo', pibo])
            time.sleep(1)
            pibo = cm.tts(bhv="do_waiting_A", string=f"준비가 됐으면 시작하자고 말해줘.")
            break
        
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 시작하자고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_B", string=f"그래애! 시작하자")
                time.sleep(1)

                pibo = cm.tts(bhv="do_joy_A", string=f"우리는 춤을 추는 유령이에요. ")
                audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_dancing.mp3", volume=-1500, background=True)
                behavior.do_dance()

                pibo = cm.tts(bhv="do_stop", string=f"음악이 멈췄어. 유령은 움직일 수 없어!")
                
                time.sleep(1)
                pibo = cm.tts(bhv="do_question_S", string=f"안 움직이고 있지? 움직이면 유령인게 들킬거야!")                

                time.sleep(1)
                pibo = cm.tts(bhv="do_joy_B", string=f"음악이 다시 나온다! 춤추자~ 우리는 음악이 나오면 춤을 추는 유령이에요~!")
                audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_dancing.mp3", volume=-1500, background=True)
                behavior.do_dance()
            
                pibo = cm.tts(bhv="do_stop", string=f"음악이 멈췄어. 유령은 움직일 수 없어! 움직이면 유령인게 들킬거야!")
                
                time.sleep(1)
                pibo = cm.tts(bhv="do_joy_A", string=f"음악이 다시 나온다! 춤추자~ 우리는 음악이 나오면 춤을 추는 유령이에요~!")
                audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_dancing.mp3", volume=-1500, background=True)
                behavior.do_dance()
                
                pibo = cm.tts(bhv="do_stop", string=f"음악이 멈췄어. 안 움직이고 있지? 움직이면 유령인게 들킬거야!")
                
                time.sleep(2)
                pibo = cm.tts(bhv="do_compliment_L", string=f"열심히 춤춘 {wm.word(self.user_name, 0)}가 최고야~ 정말 신났어! 춤추느라 힘들지는 않았어?")
                cwc.writerow(['pibo', pibo])                
                break                
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"춤추느라 힘들지는 않았어?")            
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            pibo = cm.tts(bhv="do_suggestion_L", string=f"그랬구나. 그래도 {wm.word(self.user_name, 0)}가 춤을 잘 춰서 파이보는 정말 재미있었어! ")
            time.sleep(1)
            pibo = cm.tts(bhv="do_question_S", string=f"춤 추니까 기분이 어땠어? 신났어?")            
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"춤 추니까 기분이 어땠어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_question_S", string=f"정말? 왜?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"왜 그런 기분이 들었어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_question_S", string=f"그런 이유가 있었구나. {wm.word(self.user_name, 0)}는 최고의 유령댄서였어~ 다음에는 더 재미있는 춤을 추자!")
            break

            
        pibo = cm.tts(bhv="do_stop", string=f"{wm.word(self.user_name, 0)}가 열심히 놀이를 했으니, 오늘은 술술 스탬프를 찍어줄께.")
        behavior.do_stamp()
        time.sleep(1)
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"사진을 찍어 줄게! 멋진 춤 동작을 해봐!")
        behavior.do_photo()
                
        # 3. 피드백 수집
        time.sleep(1)                   
        pibo = cm.tts(bhv='do_question_S', string="파이보랑 노는 거 재미있었어? 재밌었는지, 별로였는지 얘기해줄래?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"파이보랑 노는 거 재미있었어?")
        
        # 종료 인사
        pibo = cm.tts(bhv="do_joy_A", string=f"그럼 우리 나중에 또 놀자!")

        if len(answer[0][1]) != 0:
            for i in range(len(self.Negative)):
                if self.Negative[i] in answer[0][1]:
                    self.aa = 'negative'          
            for j in range(len(self.Positive)):
                if self.Positive[j] in answer[0][1]:
                    self.aa = 'positive'                
            if len(self.aa) == 0: 
                self.aa = 'else'
              
        if self.aa == "negative":
            cm.tts(bhv="do_joy_A", string=f"파이보는 {wm.word(self.user_name, 0)}랑 놀아서 재미있었어!")
            self.score = [-0.5, 0.0, 0.0, 0.0]
        
        if self.aa == "positive":
            cm.tts(bhv="do_joy_A", string=f"나도야! 다음에 또 재미있는 놀이 알려줄게.")
            self.score = [0.5, 0.0, 0.0, 0.0]
            
        if self.aa != "negative" and self.aa != "positive": # if answer[0][0] == "neutral":
            cm.tts(bhv="do_joy_A", string=f"{wm.word(self.user_name, 0)}랑 노는 건 정말 재미있어.")
            self.score = [-0.25, 0.0, 0.0, 0.0]
        
        cwp.writerow([today, filename, self.score[0], self.score[1], self.score[2],self.score[3]])

        # 종료 인사
        pibo = cm.tts(bhv="do_joy_A", string=f"나랑 놀아줘서 고마워~")

        # 4. Paradise framework 기록
        turns = sum((self.reject[i] + 1) * 2 for i in range(len(self.reject)))  
        reject = sum(self.reject) 
        
        cwc.writerow(['Turns', turns])
        cwc.writerow(['Rejections', reject])
        cwc.writerow(['Misrecognitions', ])

        cwc.writerow(['%Turns', ])
        cwc.writerow(['%Rejections', ])
        cwc.writerow(['%Misrecognitions', ])

        # 5. 활동 완료 기록
        today_end = datetime.now().strftime('%m%d_%H%M')        
        gss.write_sheet(name=self.user_name, today=f'end_{today_end}', activities=filename)



if __name__ == "__main__":
    
    com = Com()
    com.com_4()