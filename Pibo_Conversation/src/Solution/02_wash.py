# -*- coding: utf-8 -*-

# 문제해결-씻기 싫어

import os, sys
import re
import csv
import random
from datetime import datetime
import time
import json

# sys.path.append('/home/kiro/workspace/Conversation_Scenarios/')
sys.path.append('/home/pi/Pibo_Package_02/Pibo_Conversation/')
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
filename = os.path.basename(__file__).strip('.py')
today = datetime.now().strftime('%m%d_%H%M')
csv_conversation = open(f'{folder}/{today}_{filename}.csv', 'a', newline='', encoding = 'utf-8')
csv_preference = open(f'{folder}/aa.csv', 'a', newline='', encoding = 'utf-8')
cwc = csv.writer(csv_conversation)
cwp = csv.writer(csv_preference)
crc = csv.reader(csv_conversation, delimiter=',', doublequote=True, lineterminator='\r\n', quotechar='"')


class Solution():    
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = "예진" 
        self.score = []
        self.turns = []
        self.reject = []
                
        
    def Wash(self):
        
        # 1.1 문제 제시
        pibo = cm.tts(bhv="do_sad", string="파이보는 씻는게 정말 싫어! ")
        
        # 1.2 경험 질문
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}도 씻기 싫을 때가 있지?")
        answer = cm.responses_proc(re_bhv="do_sad", re_q=f"{wm.word(self.user_name, 0)}도 씻기 싫을 때가 있지?",
                                   pos_bhv="do_compliment_S", pos="나랑 똑같네!")    
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
     
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 씻기 싫을 때 어떻게 하니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}는 씻기 싫을 때 어떻게 하니?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])

        pibo = cm.tts(bhv="do_question_L", string="그래도 엄마는 씻어야 된다고 하시던데, 엄마는 왜 씻으라고 하실까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="친구에게 나쁜 말을 하고 싶을 때는 참는게 좋겠지?",
                                   neu_bhv="do_explain_C", neu="나쁜 말을 쓰면 기분이 안 좋아지니까 참는게 좋을 것 같아.")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])

        pibo = cm.tts(bhv="do_question_S", string="오랫동안 안 씻으면 어떻게 될까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="오랫동안 안 씻으면 어떻게 될까?",
                                   pos_bhv="do_compliment_S", pos="오랫동안 안 씻으면 몸이 아플수도 있겠다!",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 바로 떠오르지 않을 수 있어.",
                                   act_bhv="do_compliment_S", act="오랫동안 안 씻으면 몸이 아플수도 있겠다!")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
            
        pibo = cm.tts(bhv="do_question_S", string="안 씻어서 냄새가 나면 친구들이 싫어할수도 있을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="안 씻어서 냄새가 나면 친구들이 싫어할수도 있을까?",
                                   pos_bhv="do_joy_B", pos="나도 좋은 냄새가 나는 친구가 좋았던 것 같아!",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 모를 수 있어. 좋은 냄새가 나는 친구가 좋았던 것 같아!",
                                   act_bhv="do_joy_B", act="나도 좋은 냄새가 나는 친구가 좋았던 것 같아!")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
        
        # 2.1 문제 해결
        pibo = cm.tts(bhv="do_joy_A", string=f"파이보도 향기로워 지도록 잘 씻어야 겠다! {wm.word(self.user_name, 0)}도 깨끗하게 잘 씻자!")
                         
        
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
        gss.write_sheet(name=self.user_name, today=f'(4)_{today}', activities=filename)




if __name__ == "__main__":
    
    sol = Solution()
    sol.Wash()