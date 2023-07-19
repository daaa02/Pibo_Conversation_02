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

sys.path.append('/home/pi/Pibo_Play/')
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


class Mus():
    
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
                
        
    def mus_3(self):
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"빨래집게 탑 놀이를 해보자!")
        
        time.sleep(1)
        pibo = cm.tts(bhv="do_explain_A", string=f"이번 놀이는 빨래집게와 단단한 종이, 종이를 자를 가위가 필요해! 빨래집게는 많으면 많을수록 좋아.")
        cwc.writerow(['pibo', pibo])
        
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 준비 됐다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"좋았어. 놀이 방법을 알려줄께!")
                time.sleep(1)                
                pibo = cm.tts(bhv="do_explain_B", string=f"빨래집게는 힘을 주어 누르면 열려~ 엄지와 검지 손가락을 집게처럼 사용해봐.")
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
                pibo = cm.tts(bhv="do_explain_A", string=f"좋았어~ 이제 빨래집게를 연결해서 여러 모양을 만들 거야. 준비가 되면 시작하자고 말해줘~")
                cwc.writerow(['pibo', pibo])
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
                pibo = cm.tts(bhv="do_suggestion_S", string=f"빨래집게 위에 빨래집게를 꽂아 탑을 쌓아 보자.")
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"가지고 있는 집게를 남김 없이 모두 연결하는 거야. 다 했으면 다 했어 라고 말해줘.")
                cwc.writerow(['pibo', pibo])                
                break
            else:
                continue                         
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"다 했으면 다 했어 라고 말해줘!")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                time.sleep(1)
                pibo = cm.tts(bhv="do_compliment_S", string=f"정말 멋진 탑이 완성 되었는걸?")
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"이젠 새로운 모양을 만들기 위해 탑을 무너뜨려보자. 다 했으면 다 했어 라고 말해줘.")
                break
            else:
                continue      
            
        while True:            
            answer = cm.responses_proc(re_bhv="do_waiting_B", re_q=f"다 했으면 다 했어 라고 말해줘.")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                time.sleep(1)
                pibo = cm.tts(bhv="do_compliment_S", string=f"우와 정말 빠른걸?")
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"이번엔 단단한 종이를 동그라미 모양으로 자르고 가장자리에 빨래집게를 꽂아 꾸며보자. 세모나 네모 모양도 괜찮아. {wm.word(self.user_name, 0)}는 어떤 모양을 만들고 싶어?")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:            
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 어떤 모양을 만들고 싶어?")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            time.sleep(1)
            pibo = cm.tts(bhv="do_compliment_S", string=f"그렇구나~ 정말 기대된다. 그럼 시작해보자! 다 했으면 다 했다고 말해줘~")
            cwc.writerow(['pibo', pibo])
            break
        
        while True:            
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"다 했으면 다 했다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                time.sleep(1)
                pibo = cm.tts(bhv="do_compliment_L", string=f"우와아 정말 잘했다~ 사자 모양 같기도 하고 고슴도치 모양 같기도 하고 정말 재미있네!")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue  
        
        while True:
            pibo = cm.tts(bhv="do_question_S", string=f"오늘 놀이하면서 뭐가 가장 재미있었어?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"오늘 놀이하면서 뭐가 가장 재미있었어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_compliment_S", string=f"그렇구나. 파이보는 탑을 높게 높게 쌓아서 신기했어.")
            time.sleep(1)
            
            pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 뭐가 가장 기억에 남아?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 뭐가 가장 기억에 남아")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_compliment_S", string=f"알려줘서 고마워. {wm.word(self.user_name, 0)}랑 노는 건 항상 너무 재밌어~")
            break          
            
        pibo = cm.tts(bhv="do_stop", string=f"{wm.word(self.user_name, 0)}가 열심히 놀이를 했으니, 오늘은 튼튼 스탬프를 찍어줄께.")
        behavior.do_stamp()
        time.sleep(1)
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"사진을 찍어 줄게! 축구 선수처럼 포즈를 취해봐!")
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
            self.score = [0.0, 0.0, 0.0, -0.5]
        
        if self.aa == "positive":
            cm.tts(bhv="do_joy_A", string=f"나도야! 다음에 또 재미있는 놀이 알려줄게.")
            self.score = [0.0, 0.0, 0.0, 0.5]
            
        if self.aa != "negative" and self.aa != "positive": # if answer[0][0] == "neutral":
            cm.tts(bhv="do_joy_A", string=f"{wm.word(self.user_name, 0)}랑 노는 건 정말 재미있어.")
            self.score = [0.0, 0.0, 0.0, -0.25]
        
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
    
    mus = Mus()
    mus.mus_3()