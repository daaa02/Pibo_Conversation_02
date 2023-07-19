# 역할놀이-마법을 부리는 존재

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


class Cog():   
    
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

    
    def cog_12(self):
        pibo = cm.tts(bhv="do_suggestion_S", string=f"줄자 놀이를 해보자!")
        time.sleep(1)
        pibo = cm.tts(bhv="do_explain_A", string=f"이번 놀이는 줄자와 테이프, 지우개가 필요해! 준비가 되면 준비 됐다고 말해줘~")
        
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 준비 됐다고 말해줘~")
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"좋았어. 놀이 방법을 알려줄께!")
                time.sleep(1)                
                pibo = cm.tts(bhv="do_explain_B", string=f"이번 놀이는 줄자를 가지고 길이를 재 보는 놀이야. 할 수 있지? 할 수 있으면 할 수 있다고 말해줘~ ")
                cwc.writerow(['pibo', pibo])
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
                pibo = cm.tts(bhv="do_explain_A", string=f"좋았어! 집안의 여러 물건의 길이를 재 보고, 길이를 비교해 볼 거야. 준비가 됐으면 시작하자고 말해줘~") 
                time.sleep(1)
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비 됐으면 준비 됐다고 말해줘!")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_question_S", string=f"그래애 시작하자! 먼저 줄자는 어떨 때 사용하는 물건인지 이야기 해볼래?")
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"줄자는 어떨 때 사용하는 물건일까?")
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                
                pibo = cm.tts(bhv="do_suggestion_S", string=f"줄자는 길이나 거리를 잴 때 사용해. 줄자를 끝까지 펴면 길이가 얼만큼인지 알 수 있어!")
                time.sleep(1)
                
                pibo = cm.tts(bhv="do_suggestion_L", string=f"끝까지 펴보고 적혀있는 숫자를 알려줄래?")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"끝까지 펴보고 적혀있는 숫자를 알려줄래?")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_compliment_L", string=f"우와. {wm.word(self.user_name, 0)}는 큰 숫자도 잘 읽는구나!")
            time.sleep(1)
            
            pibo = cm.tts(bhv="do_waiting_C", string=f"이번엔 집안의 여러 물건의 길이를 재보자. TV, 식탁, 서랍장 처럼 {wm.word(self.user_name, 0)}가 재보고 싶은 물건을 찾아봐.")
            time.sleep(1)
            
            pibo = cm.tts(bhv="do_waiting_C", string=f"찾았으면 찾았어 라고 말하고 그 앞으로 파이보를 옮겨줘.")
            cwc.writerow(['pibo', pibo])
            break
        
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_C", re_q=f"찾았으면 찾았어 라고 말하고 그 앞으로 파이보를 옮겨줘.")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_question_S", string=f"우와, 정말 잘 찾았네! 이제 길이를 재 보자. 한 번 재어보고 알려줄래?")
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"이제 길이를 재 보자. 한 번 재어보고 알려줄래?")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                
                pibo = cm.tts(bhv="do_compliment_L", string=f"좋았어. 처음 해 보는데 정말 잘 하네! 한번 더 해보자.")
                
                time.sleep(1)
                pibo = cm.tts(bhv="do_waiting_C", string=f"{wm.word(self.user_name, 0)}가 재보고 싶은 물건을 찾아봐.")
                time.sleep(1)
                
                pibo = cm.tts(bhv="do_waiting_C", string=f"찾았으면 찾았어 라고 말하고 그 앞으로 파이보를 옮겨줘.")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_C", re_q=f"찾았으면 찾았어 라고 말하고 그 앞으로 파이보를 옮겨줘.")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_question_S", string=f"이번에도 잘 찾았네! 이제 길이를 재어보고 알려줘.")
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"길이를 재어보고 알려줘.")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                
                pibo = cm.tts(bhv="do_compliment_L", string=f"역시 길이를 정말 잘 재는구나!")                
                break
            else:
                continue        
            
        while True:
            pibo = cm.tts(bhv="do_question_L", string=f"오늘 줄자 놀이는 재미있었어?")
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"오늘 줄자 놀이는 재미있었어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_question_L", string=f" 정말? 큰 물건을 재는 게 어렵진 않았어?")
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"큰 물건을 재는 게 어렵진 않았어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_question_L", string=f"그랬구나. 파이보는 {wm.word(self.user_name, 0)}가 줄자를 다루는 모습이 멋졌어~")
            break
        
            
        pibo = cm.tts(bhv="do_stop", string=f"{wm.word(self.user_name, 0)}가 열심히 놀이를 했으니, 오늘은 똑똑 스탬프를 찍어줄께.")
        behavior.do_stamp()
        time.sleep(1)
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"사진을 찍어 줄게! 줄자를 들고 브이해봐!")        
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
            self.score = [0.0, 0.0, -0.5, 0.0]
        
        if self.aa == "positive":
            cm.tts(bhv="do_joy_A", string=f"나도야! 다음에 또 재미있는 놀이 알려줄게.")
            self.score = [0.0, 0.0, 0.5, 0.0]
            
        if self.aa != "negative" and self.aa != "positive": # if answer[0][0] == "neutral":
            cm.tts(bhv="do_joy_A", string=f"{wm.word(self.user_name, 0)}랑 노는 건 정말 재미있어.")
            self.score = [0.0, 0.0, -0.25, 0.0]
        
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
    
    cog = Cog()
    cog.cog_12()