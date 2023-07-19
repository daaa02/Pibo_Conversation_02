# -*- coding: utf-8 -*-

# 문제해결-씻기 싫어

import os, sys
import re
import csv
import time
import json
import random
from datetime import datetime

# sys.path.append('/home/kiro/workspace/Conversation_Scenarios/')
sys.path.append('/home/pi/Pibo_Conversation/')
from data.c_conversation_manage import ConversationManage, WordManage, NLP
from data.speech_to_text import speech_to_text
from data.text_to_speech import TextToSpeech, text_to_speech
from data.spread import google_spread_sheet

cm = ConversationManage()
wm = WordManage()
nlp = NLP()
audio = TextToSpeech()
gss = google_spread_sheet()

folder = "/home/pi/UserData"
filename = os.path.basename(__file__).strip('.py').strip('.py')
today = datetime.now().strftime('%y%m%d_%H%M')
csv_conversation = open(f'{folder}/{today}_{filename}.csv', 'a', newline='', encoding = 'utf-8')
csv_preference = open(f'{folder}/aa.csv', 'a', newline='', encoding = 'utf-8')
cwc = csv.writer(csv_conversation)
cwp = csv.writer(csv_preference)
crc = csv.reader(csv_conversation, delimiter=',', doublequote=True, lineterminator='\r\n', quotechar='"')



class Solution():    
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = config['user_name'] 
        self.score = []
        self.turns = []
        self.reject = []
        
    def Wash(self):
        
        # 1.1 문제 제시
        pibo = cm.tts(bhv="do_sad", string="요즘 사람들이 많은 곳이든 집 안이든 신나게 뛰어다니고 싶어.")
        
        # 1.2 경험 질문
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}도 뛰다가 넘어진 적이 있니?")
        answer = cm.responses_proc(re_bhv="do_sad", re_q=f"{wm.word(self.user_name, 0)}도 뛰다가 넘어진 적이 있니?",
                                   pos_bhv="do_compliment_S", pos="넘어져서 아팠겠다.")    
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
        
        pibo = cm.tts(bhv="do_question_L", string="사람이 많은 곳에서 뛰어다니면 위험할까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="사람이 많은 곳에서 뛰어다니면 위험할까?",
                                   pos_bhv="do_compliment_S", pos="부딪히면 아프겠지?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 부딪히면 아프겠지?")        
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
        

        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 평소에 천천히 조용히 걷니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 평소에 천천히 조용히 걷니?",
                                   pos_bhv="do_explain_C", pos="신사같은 걸?")

        pibo = cm.tts(bhv="do_question_S", string="천천히 걸으면 어떤 점이 좋을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="천천히 걸으면 어떤 점이 좋을까?",
                                   pos_bhv="do_compliment_S", pos="천천히 걸으면 안전하겠지?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어. 천천히 걸으면 안전하겠지?",
                                   act_bhv="do_compliment_S", act="천천히 걸으면 안전하겠지?")
            
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 천장에서 발소리를 들어 본 적이 있니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 천장에서 발소리를 들어 본 적이 있니?",
                                   pos_bhv="do_joy_B", pos="시끄러웠겠다!")
        
        pibo = cm.tts(bhv="do_question_L", string="어떻게 하면 발소리가 나지 않게 조용히 걸을 수 있을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="어떻게 하면 발소리가 나지 않게 조용히 걸을 수 있을까?",
                                   pos_bhv="do_compliment_S", pos="사뿐사뿐 천천히 걸어야겠지?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 대답하기 어려울 수 있어. 사뿐사뿐 천천히 걸으면 발소리가 나지 않겠지?",
                                   act_bhv="do_compliment_S", act="사뿐사뿐 천천히 걸어야겠지?")
        
        # 2.1 문제 해결
        pibo = cm.tts(bhv="do_joy_A", string="파이보도 이제 조용하고 안전하게 걸으려고 노력해야겠다. 알려줘서 정말 고마워!")
        
        
        # 3. 피드백 수집
        time.sleep(1)                   
        pibo = cm.tts(bhv="do_question_S", string="파이보랑 얘기한 거 재미있었어? 재밌었는지, 별로였는지 얘기해줄래?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"파이보랑 얘기한 거 재미있었어?") 
              
        if answer[0][0] == "negative":
            cm.tts(bhv="do_joy_A", string=f"파이보는 {wm.word(self.user_name, 0)}랑 놀아서 재미있었어!")
            self.score = [0.0, -0.5, 0.0, 0.0]
        
        if answer[0][0] == "positive":
            cm.tts(bhv="do_joy_A", string=f"나도야! 다음에 또 재미있는 놀이 알려줄게.")
            self.score = [0.0, 0.5, 0.0, 0.0]
            
        if answer[0][0] != "negative" and answer[0][0] != "positive": # if answer[0][0] == "neutral":
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
        gss.write_sheet(name=self.user_name, today=today, activities=filename)




if __name__ == "__main__":
    
    sol = Solution()
    sol.Wash()