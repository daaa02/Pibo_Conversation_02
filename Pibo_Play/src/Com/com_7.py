# -*- coding: utf-8 -*-

# 의사소통-세차장놀이

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
                
        
    def com_7(self):
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"세차장 놀이를 해보자!")
        
        time.sleep(1)
        pibo = cm.tts(bhv="do_explain_B", string=f"이번 놀이는 큰 박스랑 공, 수건이 필요해!~") 
        pibo = cm.tts(bhv="do_waiting_B", string=f"준비가 되면 준비 됐다고 말해줘~")
        cwc.writerow(['pibo', pibo])
        
        while True:
            time.sleep(2)
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 준비 됐다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"좋았어. 놀이 방법을 알려줄께!")
                time.sleep(1)
                pibo = cm.tts(bhv="do_explain_B", string=f"먼저 상자를 세워서 터널을 만들거야. {wm.word(self.user_name, 0)}가 자동차가 되어서, 터널 안에 들어가면 청소부 친구가 세차를 해줄거야.")
                cwc.writerow(['pibo', pibo])
                pibo = cm.tts(bhv="do_question_S", string=f"할 수 있지? 할 수 있으면 할 수 있다고 말해줘~")
                break
            
            if answer[0][0] == "no":
                pibo = cm.tts(bhv="do_suggestion_S", string=f"그럼 다른 놀이 하자! {wm.word(self.user_name, 0)}가 다시 내 머리를 쓰다듬어주면 돼!")
                self.score = [0.0, 0.0, 0.0, -0.25]
                cwp.writerow([today, filename, self.score[0], self.score[1], self.score[2],self.score[3]])       
                sys.exit(0)
                
            else:
                continue
        
        while True: 
            time.sleep(0.5)
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"할 수 있으면 할 수 있다고 말해줘~")
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_explain_A", string=f"세차 코스는 절약코스, 기본코스, 강력 코스가 있어. 코스에 따라서 강도가 달라질거야.")
                pibo = cm.tts(bhv="do_explain_C", string=f"자동차 역할은 어떤 세차 코스를 받을 지 이야기를 해줘야해~ 준비가 됐으면 시작하자고 말해줘.")
                cwc.writerow(['pibo', pibo])                
                break
            else:
                continue
            
        while True: 
            time.sleep(0.5)        
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 시작하자고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_B", string=f"좋아아! 시작하자")
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"자동차는 터널 안으로 들어가고 청소부는 터널 옆에 앉아줘. 준비가 됐으면 준비됐다고 말해줘.")  
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue                         
        
        #1
        while True: 
            time.sleep(7) 
            answer = cm.responses_proc(re_bhv="do_waiting_B", re_q=f"준비가 됐으면 준비됐다고 말해줘. ")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_B", string=f"좋아. 세차코스는 절약코스, 기본코스, 강력코스가 있어. 원하는 세차 코스를 이야기하고 ")
                pibo = cm.tts(bhv="do_stop", string=f"시작! 이라고 말해줘. ")
                break
            else:
                continue
    
        while True:      
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"원하는 세차 코스를 이야기하고 시작!이라고 말해줘. ")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_magician.wav", volume=-1500, background=False)
            pibo = cm.tts(bhv="do_explain_B", string=f"세차가 시작됐어. 먼저 공으로 자동차 마사지를 해보자.")
            time.sleep(5)
            
            pibo = cm.tts(bhv="do_explain_B", string=f"이번에는 왁스칠을 할거야. 자동차를 수건으로 닦자.")
            time.sleep(5)            

            audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_magician.wav", volume=-1500, background=False)
            pibo = cm.tts(bhv="do_explain_B", string=f"세차가 완료됐어. 자동차는 터널에서 나와서 세차완료라고 말해줘~")      
            break       
        
        
        while True: 
            answer = cm.responses_proc(re_bhv="do_waiting_B", re_q=f"자동차는 터널에서 나와서 세차완료라고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_B", string=f"정말 깨끗해 졌는걸?")
                pibo = cm.tts(bhv="do_explain_A", string=f"이번에는  역할을 바꿔보자. 친구가 자동차, {wm.word(self.user_name, 0)}가 청소부야. 준비가 완료되면 준비됐어 라고 말해줘")
                break
            else:
                continue

        #2
        while True: 
            time.sleep(7) 
            answer = cm.responses_proc(re_bhv="do_waiting_B", re_q=f"준비가 됐으면 준비됐다고 말해줘. ")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_B", string=f"좋아. 세차코스는 절약코스, 기본코스, 강력코스가 있어. 원하는 세차 코스를 이야기하고 ")
                pibo = cm.tts(bhv="do_stop", string=f"시작! 이라고 말해줘. ")
                break
            else:
                continue
    
        while True:      
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"원하는 세차 코스를 이야기하고 시작!이라고 말해줘. ")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_magician.wav", volume=-1500, background=False)
            pibo = cm.tts(bhv="do_explain_B", string=f"세차가 시작됐어. 먼저 공으로 자동차 마사지를 해보자.")
            time.sleep(5)
            
            pibo = cm.tts(bhv="do_explain_B", string=f"이번에는 왁스칠을 할거야. 자동차를 수건으로 닦자.")
            time.sleep(5)            

            audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_magician.wav", volume=-1500, background=False)
            pibo = cm.tts(bhv="do_explain_B", string=f"세차가 완료됐어. 자동차는 터널에서 나와서 세차완료라고 말해줘~")      
            break       
            
        
        while True: 
            answer = cm.responses_proc(re_bhv="do_waiting_B", re_q=f"자동차는 터널에서 나와서 세차완료라고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_B", string=f"이번에도 정말 깨끗하게 세차가 됐는 걸?")
                break
            else:
                continue
        
        while True: 
            answer = cm.responses_proc(re_bhv="do_waiting_B", re_q=f"또 하고 싶으면 또 하자고 말해줘.")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "no" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"자동차가 정말 반짝반짝해진 것 같아. 수고했어!")
                break
            else:
                continue
                
            
        while True:  
            pibo = cm.tts(bhv="do_compliment_S", string=f"세차를 해보니까 기분이 어땠어? 상쾌해진 기분이야?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"세차를 해보니까 기분이 어땠어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_compliment_S", string=f"그렇구나. {wm.word(self.user_name, 0)}이는 어떤 코스가 제일 마음에 들었어?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"어떤 코스가 제일 마음에 들었어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_joy_A", string=f"맞아. {wm.word(self.user_name, 0)}가 정말 신나 보였어.")
            
            break
            
            
        pibo = cm.tts(bhv="do_stop", string=f"{wm.word(self.user_name, 0)}가 열심히 놀이를 했으니, 오늘은 술술 스탬프를 찍어줄께.")
        behavior.do_stamp()
        time.sleep(1)
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"사진을 찍어 줄게! 박스 안에 들어가서 브이해봐!")        
        behavior.do_photo()
        
        
        # 3. 피드백 수집
        time.sleep(1)                   
        pibo = cm.tts(bhv='do_question_S', string="파이보랑 노는 거 재미있었어? 재밌었는지, 별로였는지 얘기해줄래?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"파이보랑 노는 거 재미있었어?")
        
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
        gss.write_sheet(name=self.user_name, today=f'(4)_{today}', activities=filename)
        



if __name__ == "__main__":
    
    com = Com()
    com.com_7()
