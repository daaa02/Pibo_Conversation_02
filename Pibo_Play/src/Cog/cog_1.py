# 역할놀이-마법을 부리는 존재

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

    
    def cog_1(self):
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"휴지길 놀이를 해보자!")
        time.sleep(1)
        pibo = cm.tts(bhv="do_explain_A", string=f"놀이를 위해 휴지가 필요해! 두루마리 휴지를 준비해줘! 많으면 많을 수록 좋아. 준비가 되면 준비 됐다고 말해줘~")
        
        while True:
            time.sleep(1)  
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 준비 됐다고 말해줘~")
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"좋았어. 놀이 방법을 알려줄께!")
                time.sleep(1)                
                pibo = cm.tts(bhv="do_explain_B", string=f"휴지를 풀어서 길을 만들어 볼 거야. 어렵지 않지?")
                cwc.writerow(['pibo', pibo])
                pibo = cm.tts(bhv="do_question_S", string=f"할 수 있으면 할 수 있다고 말해줘~")
                break
            
            if answer[0][0] == "no":
                pibo = cm.tts(bhv="do_suggestion_S", string=f"그럼 다른 놀이 하자! {wm.word(self.user_name, 0)}가 다시 내 머리를 쓰다듬어주면 돼!")
                self.score = [0.0, 0.0, 0.0, -0.25]
                cwp.writerow([today, filename, self.score[0], self.score[1], self.score[2],self.score[3]])       
                sys.exit(0)
                
            else:
                continue
        
        while True:
            time.sleep(1)  
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"할 수 있으면 할 수 있다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_explain_A", string=f"좋았어! 휴지 길은 미끄러울 수 있어서 뛰면 안돼. 준비 됐으면 준비 됐다고 말해줘!")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            time.sleep(1)  
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비 됐으면 준비 됐다고 말해줘!")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_explain_A", string=f"그래애, 시작하자!")
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_S", string=f"먼저 곳곳에 휴지 섬을 만들자. 휴지를 통째로 놓고 쌓아줘! 다 만들었으면 다 만들었다고 말해줘~")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            time.sleep(10)  
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"다 만들었으면 다 만들었다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_compliment_L", string=f"정말 멋진 섬이 완성 되었는걸? 휴지로 만들어서 포근해 보여")
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_S", string=f"이제 섬끼리 연결되는 휴지 길을 만들어보자. 휴지를 풀어서 만들어줘~ 다 만들었으면 다 만들었다고 말해줘~")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            time.sleep(1)  
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"다 만들었으면 다 만들었다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_compliment_L", string=f"우와~ 멋진 휴지 세상이 완성되었네! 휴지 세상을 만들어준 {wm.word(self.user_name, 0)} 최고야~ 정말 신났어!")
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"이제 입으로 바람을 만들어서 휴지를 날려보자. ")
                time.sleep(5)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"휴지를 찢어서 휴지 섬에 눈을 내려보자. 끝났으면 끝났다고 말해줘~") 
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
            
        while True:
            time.sleep(5)  
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"끝났으면 끝났다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_question_L", string=f"휴지 눈이 내리니까 정말 포근하다~ {wm.word(self.user_name, 0)}는 언제 포근함을 느껴?")
                answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}는 언제 포근함을 느껴?")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                
                pibo = cm.tts(bhv="do_question_S", string=f"정말? 왜 포근해?")
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"왜 포근해?")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                
                pibo = cm.tts(bhv="do_question_S", string=f"그렇구나~ 생각만 해도 기분이 좋아.")                
                break
            else:
                continue
            
        pibo = cm.tts(bhv="do_stop", string=f"{wm.word(self.user_name, 0)}가 열심히 놀이를 했으니, 오늘은 똑똑 스탬프를 찍어줄께.")
        behavior.do_stamp()
        
        time.sleep(1.5)
        pibo = cm.tts(bhv="do_suggestion_S", string=f"사진을 찍어 줄게! 휴지섬 앞에 서서 포즈를 취해봐!")        
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
    cog.cog_1()