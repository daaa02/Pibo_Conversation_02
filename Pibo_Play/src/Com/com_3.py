# -*- coding: utf-8 -*-

# 사회기술-차례대로 순서를 지켜요

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
                
        
    def com_3(self):
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"뒤로 웃고 미끄러지는 거리 놀이를 해보자!")
        
        time.sleep(1)
        pibo = cm.tts(bhv="do_explain_A", string=f"이번 놀이는 종이랑 그림 도구, 테이프가 필요해! 준비가 되면 준비 됐어 라고 말해줘~")
        cwc.writerow(['pibo', pibo])
        
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 준비 됐다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"좋았어. 놀이 방법을 알려줄께!")
                time.sleep(1)                
                pibo = cm.tts(bhv="do_explain_B", string=f"화장실, 부엌, 현관에 새로운 이름을 만들어보자. 만약에 화장실 이름을 박수치는 거리로 만들면, 화장실 앞에 도착할 때 박수를 쳐야해.")
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
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"할 수 있으면 할 수 있다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_explain_A", string=f"거리 이름은 수영하는 거리도 될 수 있고, 등산하는 거리, 피아노 치는 거리 거리처럼 다양하게 지을 수 있어.")
                cwc.writerow(['pibo', pibo])
                pibo = cm.tts(bhv="do_stop", string=f"시작해볼까? 준비가 되면 시작하자고 말해줘~")
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 시작하자고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_B", string=f"그래애! 시작하자")
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"장소 마다 이름을 정해보자~ 먼저 화장실은 무슨 거리라고 할까?")  
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue                         
        
        while True:
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"화장실은 무슨 거리라고 할까?")            
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_question_S", string=f"좋았어! 그럼 부엌은 뭐라고 할까?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"부엌은 무슨 거리라고 할까?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_question_S", string=f"멋진데? 그럼 현관은 뭐라고 할까?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"현관은 무슨 거리라고 할까?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_joy_B", string=f"좋았어! 이제 종이랑 그림 도구로 장소마다 표지판을 만들어 보자.")
            time.sleep(1)
            pibo = cm.tts(bhv="do_waiting_A", string=f"거리 이름을 그림으로 표현하거나 글씨로 써서 표지판을 완성해줘~ 세 개 모두 완성 했으면 다 했어 라고 말해줘.")
            cwc.writerow(['pibo', pibo])
        
            break
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"거리 이름을 그림으로 표현하거나 글씨로 써서 표지판을 완성해줘~ 세 개를 모두 완성 했으면 다 했어 라고 말해줘.")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_compliment_S", string=f"멋진 표지판이 완성되었네.")
                time.sleep(1)
                pibo = cm.tts(bhv="do_waiting_B", string=f"이제 거리에 표지판을 붙이자~ 다 붙이면 다 붙였다고 말해줘")  
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"다 붙이면 다 붙였다고 말해줘!")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_question_S", string=f"좋았어. 먼저 어떤 거리로 가볼까? ")
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"먼저 어떤 거리로 가볼까? ")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                
                pibo = cm.tts(bhv="do_compliment_S", string=f"그래! 파이보를 데려가 줄래? 도착하면 도착했어 라고 말해줘~")  
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"도착하면 도착했어 라고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_question_S", string=f"좋았어. 이제 거리 이름처럼 흉내 내 보자!")
                audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_standing.mp3", volume=-1500, background=False)  
                
                pibo = cm.tts(bhv="do_compliment_L", string=f"정말 열심히 잘 표현하는 걸? 또 어떤 거리를 가볼까?")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"또 어떤 거리를 가볼까?")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_compliment_S", string=f"그래! 파이보를 데려가 줄래? 도착하면 도착했어 라고 말해줘~")  
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"도착하면 도착했어 라고 말해줘~")            
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_question_S", string=f"좋았어. 이제 거리 이름처럼 흉내 내 보자!")
                audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_standing.mp3", volume=-1500, background=False)
                
                pibo = cm.tts(bhv="do_compliment", string=f"거리 이름에 따라 정말 열심히 표현했어~우리만의 멋진 동네를 만든 것 같아!")
                time.sleep(1)
                
                pibo = cm.tts(bhv="do_suggestion_L", string=f"이제 자리에 앉아 잠시 쉬어보자!")
                time.sleep(3)
                
                pibo = cm.tts(bhv="do_suggestion_L", string=f"놀이가 어렵지는 않았어?")
                answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"놀이가 어렵지는 않았어?")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                
                pibo = cm.tts(bhv="do_suggestion_L", string=f"그랬구나. 처음해보는 건 원래 쉽지 않아. 하지만 {wm.word(self.user_name, 0)}의 열심히 하는 모습은 정말 멋졌어!")
                time.sleep(1)
                
                pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 어떤 거리가 제일 재미있었어?")
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"어떤 거리가 제일 재미있었어?")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                
                pibo = cm.tts(bhv="do_question_S", string=f"정말? 왜?")
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"왜 그 거리가 제일 재미있었어?")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                
                pibo = cm.tts(bhv="do_question_S", string=f"그렇구나~ 파이보는 {wm.word(self.user_name, 0)}랑 갔던 거리가 다 재미있었어~")
                break
            else:
                continue             
            
        pibo = cm.tts(bhv="do_stop", string=f"{wm.word(self.user_name, 0)}가 열심히 놀이를 했으니, 오늘은 술술 스탬프를 찍어줄께.")
        behavior.do_stamp()
        time.sleep(1)
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"사진을 찍어 줄게! 거리를 걷는 자세를 취해봐!")
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
        today_end = datetime.now().strftime('%m%d_%H%M')        
        gss.write_sheet(name=self.user_name, today=f'end_{today_end}', activities=filename)


if __name__ == "__main__":
    
    com = Com()
    com.com_3()