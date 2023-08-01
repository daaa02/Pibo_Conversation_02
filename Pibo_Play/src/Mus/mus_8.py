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
                
        
    def mus_8(self):
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"요리사 훈련 놀이를 해보자!")
        
        time.sleep(1)
        pibo = cm.tts(bhv="do_explain_A", string=f"이번 놀이는 나무주걱, 테이프, 소프트볼이 필요해! 소프트볼이 없으면 풍선을 작게 불어서 묶어도 돼.")
        cwc.writerow(['pibo', pibo])
        
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 준비 됐다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"좋았어. 놀이 방법을 알려줄께!")
                time.sleep(1)                
                pibo = cm.tts(bhv="do_explain_B", string=f"나무로 된 주걱이 요리사 도구야. 주걱 위에 놓인 호박을 풍선이라 생각하고 떨어트리지 않고 운반하는 거야. ")
                cwc.writerow(['pibo', pibo])
                pibo = cm.tts(bhv="do_question_S", string=f"어렵지 않지? 할 수 있으면 할 수 있다고 말해줘~")
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
                pibo = cm.tts(bhv="do_explain_A", string=f"좋았어! 요리사는 체력 연습도 할 수 있어. 주걱 위에 풍선을 올려놓고 앉았다 일어서는 연습을 하는 거야. 준비가 되면 시작하자고 말해줘~")
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
                pibo = cm.tts(bhv="do_suggestion_S", string=f"우선 목표점과 출발선을 정해야 해. 출발할 위치에 테이프를 붙이고, 도착할 목표점에도 테이프를 붙이면 돼. 다 했으면 다 했어 라고 말해줘.")
                cwc.writerow(['pibo', pibo])                
                break
            else:
                continue                         
            
        while True:
            time.sleep(5)
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"다 했으면 다 했어 라고 말해줘!")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"잘했어! 이젠 공을 호박이라고 생각하고 재료를 들고 출발점에서 목표점까지 움직여보자~ 다 했으면 다 했어 라고 말해줘.")
                break
            else:
                continue      
            
        while True:      
            audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_body.mp3", volume=-1500)   
            answer = cm.responses_proc(re_bhv="do_waiting_B", re_q=f"다 했으면 다 했어 라고 말해줘.")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                audio.stop
                time.sleep(1)
                pibo = cm.tts(bhv="do_compliment_S", string=f"우와 정말 빠른걸? 이제 체력 연습을 해보자!")
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"주걱 위에 공을 올리고 앉았다 일어나는 거야. 앉을 준비가 됐으면 준비 됐어 라고 말해줘!")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:            
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"앉을 준비가 됐으면 준비 됐어 라고 말해줘!")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                time.sleep(1)
                pibo = cm.tts(bhv="do_compliment_S", string=f"좋았어! 내가 천천히 열까지 셀 동안 해보는 거야. 중간에 공을 떨어뜨리면 다시 시작해도 돼.")
                time.sleep(1)
                pibo = cm.tts(bhv="do_compliment_S", string=f"몇 번 성공했는지 세었다가 알려줘. 그럼 준비이~ 시이작!")
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_S", string=f"하나, 두울, 세엣, 네엣, 다섯, 여섯, 일곱, 여덟, 아홉, 열!")
                time.sleep(1)
                cm.tts(bhv="do_question_L", string=f"이제 그만~ 몇 번 성공 했어?")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
        
        while True:            
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"몇 번 성공 했어?")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            pibo = cm.tts(bhv="do_compliment_L", string=f"익숙하지 않았을 텐데 대단해! {wm.word(self.user_name, 0)}가 다리가 더 튼튼해진 것 같아!")
            break
        
        while True:
            time.sleep(1)
            pibo = cm.tts(bhv="do_question_S", string=f"정말 멋진 요리사 훈련 놀이였어. 요리사 훈련 해 보니까 진짜 요리사가 된 기분이 들었어?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"요리사 훈련 해 보니까 진짜 요리사가 된 기분이 들었어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_compliment_S", string=f"그렇구나. 오늘 놀이에서 어려운 게 있었어?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"오늘 놀이에서 어려운 게 있었어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_question_S", string=f"그렇구나. 풍선을 안 떨어트리려고 할 때 힘이 많이 들것 같았어. {wm.word(self.user_name, 0)}는 어땠어? ")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"풍선을 안 떨어트리려고 할 때 힘이 많이 들것 같았어. {wm.word(self.user_name, 0)}는 어땠어? ")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_compliment_S", string=f"우와아~ 그래도 멋지게 해냈구나. {wm.word(self.user_name, 0)}가 힘들어도 끝까지 하는 모습이 보기 좋았어~")
            break          
            
        pibo = cm.tts(bhv="do_stop", string=f"{wm.word(self.user_name, 0)}가 열심히 놀이를 했으니, 오늘은 튼튼 스탬프를 찍어줄께.")
        behavior.do_stamp()
        time.sleep(1)
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"사진을 찍어 줄게! 주걱을 멋지게 들고 브이를 해봐!")
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
        gss.write_sheet(name=self.user_name, today=f'(4)_{today}', activities=filename)


if __name__ == "__main__":
    
    mus = Mus()
    mus.mus_8()