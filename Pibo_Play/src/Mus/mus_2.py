# -*- coding: utf-8 -*-

# 대근육-미라

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
        
        
    def mus_2(self):
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"미이라 만들기 놀이를 해보자!")
        
        time.sleep(1)
        pibo = cm.tts(bhv="do_explain_A", string=f"이번 놀이는 휴지가 필요해~ 두루마리 휴지를 준비해줘.")
        pibo = cm.tts(bhv="do_explain_B", string=f"준비가 되면 준비 됐어 라고 말해줘~")
        cwc.writerow(['pibo', pibo])
        
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 준비 됐다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"좋았어. 놀이 방법을 알려줄께!")
                time.sleep(1)                
                pibo = cm.tts(bhv="do_explain_B", string=f"친구와 함께 미라를 만들어 볼 거야. 미라는 휴지로 몸을 돌돌 감아서 만들 수 있어!")
                cwc.writerow(['pibo', pibo])
                
                pibo = cm.tts(bhv="do_question_S", string=f"할 수 있지? 할 수 있으면 할 수 있어~ 라고 말해줘.")
                break
            
            if answer[0][0] == "no":
                pibo = cm.tts(bhv="do_suggestion_S", string=f"그럼 다른 놀이 하자! {wm.word(self.user_name, 0)}가 다시 내 머리를 쓰다듬어주면 돼!")
                self.score = [0.0, 0.0, 0.0, -0.25]
                cwp.writerow([today, filename, self.score[0], self.score[1], self.score[2],self.score[3]])                   
                sys.exit(0)
                
            else:
                continue
            
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"할 수 있으면 할 수 있어 라고 말해줘.")
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_explain_A", string=f"{wm.word(self.user_name, 0)}가 먼저 미라가 되어보자. 미라가 되려면 다른 사람이 휴지로 잘 감쌀 수 있도록 움직이지 않고 기다려줘야해")
                pibo = cm.tts(bhv="do_question_S", string=f"할 수 있지? 할 수 있으면 할 수 있어라고 말해줘")
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"할 수 있으면 할 수 있어 라고 말해줘.")
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                    pibo = cm.tts(bhv="do_question_L", string=f"좋았어! 서로 힘을 합쳐 미라를 완성해봐.")
                    time.sleep(1)
                    pibo = cm.tts(bhv="do_suggestion_S", string=f"휴지를 길게 사용하면 더 쉬워. 천천히 시작해봐~ 그럼 내가 3분을 세어 볼게. 시이~작!")
                    time.sleep(10)
                    break
            else:
                continue
                
        while True:
            pibo = cm.tts(bhv="do_question_S", string=f"땡~! 다 했어?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"다 했어?")
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string="우와, 멋진 미라가 되었는데?")
                
            if answer[0][0] == "no":
                pibo = cm.tts(bhv="do_suggestion_S", string="시간이 더 필요한가 보구나. 천천히 해봐. 다했으면 다 했다고 말해줘~")
                time.sleep(5)
                answer = cm.responses_proc(re_bhv="do_suggestion_L", re_q=f"다했으면 다 했다고 말해줘~")
                
                if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                    pibo = cm.tts(bhv="do_joy_A", string="우와, 멋진 미라가 되었는데?")
                    
            time.sleep(1)
            break
        
        
        while True:    
            pibo = cm.tts(bhv="do_suggestion_L", string=f"이제 휴지를 마음껏 찢어보자. 다했으면 다 했다고 말해줘~")
            answer = cm.responses_proc(re_bhv="do_suggestion_L", re_q=f"다했으면 다 했다고 말해줘~")
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_suggestion_L", string=f"이제 자리에 누워보자. 뜯어진 휴지를 몸 위에 덮고 잠시 휴식을 취해봐. 누워서 준비 됐으면 준비 됐다고 말해줘.")                
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"누워서 준비 됐으면 준비 됐다고 말해줘!")
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_B", string=f"정말 편안하겠다. 1분 간 그대로 있어!") 
                time.sleep(5)                
                break
            else:
                continue
            
        while True:
            pibo = cm.tts(bhv="do_compliment_S", string=f"정말 재치있는 미라 만들기 놀이었어. 휴지로 감싸는 게 어려웠을 텐데, 열심히 하는 모습이 보기 좋았어!")
            cwc.writerow(['pibo', pibo])

            pibo = cm.tts(bhv="do_question_S", string=f"휴지를 덮고 있으니 어떤 생각이 들어?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"휴지를 덮고 있으니 어떤 생각이 들어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            
            pibo = cm.tts(bhv="do_compliment_S", string=f"그랬구나. 파이보는 잠이 올 것만 같아.. {wm.word(self.user_name, 0)}는 미라를 만들 때 기분이 어땠어?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 미라를 만들 때 기분이 어땠어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            
            pibo = cm.tts(bhv="do_question_S", string=f"그렇구나. 파이보도 그랬어! 휴지를 뜯을 땐 기분이 어땠어?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"휴지를 뜯을 땐 기분이 어땠어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            
            pibo = cm.tts(bhv="do_joy_B", string=f"생각만 해도 기분 좋다~!")
            
            break
        
        
        pibo = cm.tts(bhv="do_stop", string=f"{wm.word(self.user_name, 0)}가 열심히 놀이를 했으니, 오늘은 튼튼 스탬프를 찍어줄께.")
        behavior.do_stamp()
        time.sleep(1)
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"사진을 찍어 줄게! 미라 흉내를 내며 포즈를 취해봐!")
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
    time.sleep(5)
    mus = Mus()
    mus.mus_2()
    