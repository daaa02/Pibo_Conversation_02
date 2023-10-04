# -*- coding: utf-8 -*-

# 사회기술-큰 소리로 이야기 하거나 통화하지 않아요

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


class Soc():
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = config['user_name'] 
        self.place = ['화장실', '부엌', '현관', '큰방', '작은방']
        self.aa = ''
        self.score = []
        self.turns = []
        self.reject = []
        
        self.Positive = ['pos', '좋아', '좋은', '좋았', '좋다', '재미있', '재미 있', '재밌', '재밌어']
        self.Negative = ['neg', '별로', '아니', '안 해', '안해', '안 할래', '안 하', '싫어', '싫', '재미없', '재미 없']
        self.Neutral = ['neu', '글쎄', '몰라', '모르', '몰라', '몰랐', '보통']  
                
        
    def soc_6(self):
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"장님 안내하기 놀이를 해보자!")
        
        time.sleep(1)
        pibo = cm.tts(bhv="do_explain_A", string=f"이번 놀이는 준비물이 필요없어. 놀이 방법을 알려줄께!") 
        time.sleep(1)
        pibo = cm.tts(bhv="do_joy_A", string=f"이번 놀이에서는 파이보가 장님 역할을 할거야. 파이보가 목적지를 말하면 {wm.word(self.user_name, 0)}는 파이보를 안고 목적지에 데려다 줘.")
        cwc.writerow(['pibo', pibo])
        
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"어렵지 않지? 할 수 있으면 할 수 있다고 말해줘")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_explain_B", string=f"목적지에 도착하면 주변에 어떤 물건들이 있는지 파이보에게 알려줘. 준비 됐으면 시작하자고 말해줘.")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 시작하자고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_B", string=f"그래애! 시작하자!")
                time.sleep(1)
                
                place = random.choice(self.place)
                pibo = cm.tts(bhv="do_joy_A", string=f"먼저 {place}에 가보자! 도착하면 도착했어 라고 말해줘~")
                cwc.writerow(['pibo', pibo])
                time.sleep(7)
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"도착하면 도착했어 라고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_question_L", string=f" 빠르게 도착했는걸? {place}이 어떻게 생겼는지 알고 싶어. {place}에는 무슨 색깔이 있어?")
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{place}에는 무슨 색깔이 있어?")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                
                pibo = cm.tts(bhv="do_question_S", string=f"그렇구나! 왼쪽에는 어떤 물건이 있어?")
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"왼쪽에는 어떤 물건이 있어?")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                
                pibo = cm.tts(bhv="do_question_S", string=f"오른쪽에는 어떤 물건이 있어?")
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"오른쪽에는 어떤 물건이 있어?")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                
                pibo = cm.tts(bhv="do_question_S", string=f"바닥에도 물건이 있어?")
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"바닥에도 물건이 있어?")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])

                pibo = cm.tts(bhv="do_joy_A", string=f"{wm.word(self.user_name, 0)}는 정말 설명을 잘해주는 구나! 눈이 안보여도 {place}이 어떻게 생겼는지 알 것 같아! 친절하게 알려줘서 고마워!")
                break
            else:
                continue
            
        while True:            
            pibo = cm.tts(bhv="do_question_S", string=f"목적지 장소를 설명하는게 어렵지는 않았어?")            
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"목적지 장소를 설명하는게 어렵지는 않았어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_joy_A", string=f"그래도 정말 실감나게 잘 알려줬는걸? {wm.word(self.user_name, 0)} 덕분에 목적지를 잘 상상할 수 있었어!")
            
            time.sleep(1)
            pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 앞이 안보이면 어떨 것 같아?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"앞이 안보이면 어떨 것 같아?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_joy_A", string=f"그렇게 생각했구나. 파이보는 조금 무서웠지만, {wm.word(self.user_name, 0)}랑 있어서 안심이 됐어.")
            break
            
            
        pibo = cm.tts(bhv="do_stop", string=f"{wm.word(self.user_name, 0)}가 열심히 놀이를 했으니, 오늘은 바른 스탬프를 찍어줄께.")
        behavior.do_stamp()
        time.sleep(1)
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"사진을 찍어 줄게! 브이 해봐!")
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
            self.score = [0.0, -0.5, 0.0, 0.0]
        
        if self.aa == "positive":
            cm.tts(bhv="do_joy_A", string=f"나도야! 다음에 또 재미있는 놀이 알려줄게.")
            self.score = [0.0, 0.5, 0.0, 0.0]
            
        if self.aa != "negative" and self.aa != "positive": # if answer[0][0] == "neutral":
            cm.tts(bhv="do_joy_A", string=f"{wm.word(self.user_name, 0)}랑 노는 건 정말 재미있어.")
            self.score = [0.0, -0.25, 0.0, 0.0]
        
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
    
    soc = Soc()
    soc.soc_6()