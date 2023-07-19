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
        self.aa = ''
        self.score = []
        self.turns = []
        self.reject = []
        
        self.Positive = ['pos', '좋아', '좋은', '좋았', '좋다', '재미있', '재미 있', '재밌', '재밌어']
        self.Negative = ['neg', '별로', '아니', '안 해', '안해', '안 할래', '안 하', '싫어', '싫', '재미없', '재미 없']
        self.Neutral = ['neu', '글쎄', '몰라', '모르', '몰라', '몰랐', '보통']  
                
        
    def soc_4(self):
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"털실 놀이를 해보자!")
        
        time.sleep(1)
        pibo = cm.tts(bhv="do_explain_A", string=f"이번 놀이는 털실이랑 짧은 막대기가 필요해! ") 
        time.sleep(1)
        pibo = cm.tts(bhv="do_waiting_A", string=f"나무젓가락이나 연필을 준비하면 좋아. 준비가 되면 준비 됐어 라고 말해줘~")
        cwc.writerow(['pibo', pibo])        
        
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 준비 됐다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"좋았어. 놀이 방법을 알려줄께!")
                time.sleep(1)
                pibo = cm.tts(bhv="do_explain_B", string=f"이번 놀이는 털실을 빨리 감아보는 놀이야. 먼저 막대기에 털실을 감아 보자~ 털실을 다 감으면 털실을 풀었다가 다시 감아볼 거야.")
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
                pibo = cm.tts(bhv="do_explain_A", string=f"{wm.word(self.user_name, 0)}가 털실을 감는 동안 파이보가 시간을 재서 얼마나 걸렸는지 알려줄게. 준비가 되면 시작하자고 말해줘~")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 시작하자고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_B", string=f"그래애! 막대기에 털실을 감아보자!")
                time.sleep(1)
                
            break
        
        while True:
            pibo = cm.tts(bhv="do_suggestion_L", string=f"털실을 다 감으면 파이보에게 다 했어 라고 말해줘~ 준비 시작~!")
            start = time.time()
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"털실을 다 감으면 다 했다고 말해줘~")
            cwc.writerow(['pibo', pibo])            

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                pibo = cm.tts(bhv="do_joy_B", string=f"{int(time.time() - start)}초가 걸렸어! 정말 열심히 감았는 걸?")
                time.sleep(1)

                pibo = cm.tts(bhv="do_stop", string=f"이번에는 털실을 풀면서 뒤로 걸어가보자. 장애물에 부딪치거나 넘어지지 않게 조심해야 해. 털실을 다 풀면 다 풀었어 라고 말해줘~")
                cwc.writerow(['pibo', pibo])                
                break
            else:
                continue
        
        while True:       
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"털실을 다 풀면 다 풀었어 라고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_compliment_S", string=f"는 뒤로 걷기도 잘하는 구나!")
                break
            else:
                continue
            
        while True:
            pibo = cm.tts(bhv="do_suggestion_L", string=f"이번엔 다시 털실을 감아보자. 시작하자고 말하면 파이보가 그때부터 시간을 재도록 할게.")
            start = time.time()
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"털실을 다 감으면 다 했다고 말해줘~")
            cwc.writerow(['pibo', pibo])            

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                pibo = cm.tts(bhv="do_joy_B", string=f"{int(time.time() - start)}초가 걸렸어! 정말 빠른 속도야! 대단해~")
                break            
            else:
                continue                          
            
        while True:            
            pibo = cm.tts(bhv="do_question_S", string=f"털실을 풀면서 뒤로 걸으니까 어땠어? 어렵진 않았어?")            
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"털실을 풀면서 뒤로 걸으니까 어땠어? 어렵진 않았어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_question_L", string=f"원래 뒤로 걷는건 쉽지 않아. 하지만 오늘 {wm.word(self.user_name, 0)}는 조심조심 잘 걷던걸?")
            
            time.sleep(1)
            pibo = cm.tts(bhv="do_question_S", string=f"어떻게 하면 털실을 더 빨리 감을 수 있을까?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"어떻게 하면 털실을 더 빨리 감을 수 있을까?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_compliment_S", string=f"그럴 수 있겠구나. 파이보는 빨리 움직일 수 있는 {wm.word(self.user_name, 0)}가 너무 부러워~")
            break
            
            
        pibo = cm.tts(bhv="do_stop", string=f"{wm.word(self.user_name, 0)}가 열심히 놀이를 했으니, 오늘은 바른 스탬프를 찍어줄께.")
        behavior.do_stamp()
        time.sleep(1)
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"사진을 찍어 줄게! 털실을 들고 브이해봐!")
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
        today_end = datetime.now().strftime('%m%d_%H%M')        
        gss.write_sheet(name=self.user_name, today=f'end_{today_end}', activities=filename)


if __name__ == "__main__":
    
    soc = Soc()
    soc.soc_4()