# -*- coding: utf-8 -*-

# 문제해결-나쁜 말을 쓰게 돼

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
                
        
    def Badword(self):
        
        # 1.1 문제 제시
        pibo = cm.tts(bhv="do_sad", string="고민이 있어. 요즘 나도 모르게 나쁜 말을 자꾸 쓰는 것 같아.")
        
        # 1.2 경험 질문
        pibo = cm.tts(bhv="do_sad", string=f"파이보가 {wm.word(self.user_name, 0)}에게도 나쁜 말을 쓰면 기분이 어떨 것 같니?")
        answer = cm.responses_proc(re_bhv="do_sad", re_q=f"파이보가 {wm.word(self.user_name, 0)}에게도 나쁜 말을 쓰면 기분이 어떨 것 같니?",
                                   neg_bhv="do_compliment_S", neg=f"{wm.word(self.user_name, 0)}의 기분이 안 좋겠지?",
                                   act_bhv="do_compliment_S", act=f"{wm.word(self.user_name, 0)}의 기분이 안 좋겠지?")    

        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}가 나쁜 말을 쓰면 다른 친구들은 기분이 어떨까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}가 나쁜 말을 쓰면 다른 친구들은 기분이 어떨까?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 상상하기 어려울 수 있어.",
                                   neg_bhv="do_compliment_S", neg="친구들도 기분이 안 좋겠지?",
                                   act_bhv="do_compliment_S", act="친구들도 기분이 안 좋겠지?")

        pibo = cm.tts(bhv="do_question_S", string="친구에게 나쁜 말을 하고 싶을 때는 참는게 좋겠지?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="친구에게 나쁜 말을 하고 싶을 때는 참는게 좋겠지?",
                                   neu_bhv="do_explain_C", neu="나쁜 말을 쓰면 기분이 안 좋아지니까 참는게 좋을 것 같아.")

        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)} 주변에는 기분 좋은 말을 누가 가장 많이 하니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)} 주변에는 기분 좋은 말을 누가 가장 많이 하니?",
                                   pos_bhv="do_compliment_S", pos="나도 배우고 싶은 걸?")
        
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 어떤 말을 들으면 가장 기분이 좋니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 어떤 말을 들으면 가장 기분이 좋니?",
                                   pos_bhv="do_joy_B", pos="기분이 좋았겠다!",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 바로 떠오르지 않을 수 있어.")
            
        pibo = cm.tts(bhv="do_question_L", string="나는 척척박사라는 말을 들으면 기분이 좋아! 기분 좋은 말에는 또 뭐가 있을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="나는 척척박사라는 말을 들으면 기분이 좋아! 기분 좋은 말에는 또 뭐가 있을까?",
                                   pos_bhv="do_joy_B", pos="듣기만 해도 행복한 걸?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어.",
                                   act_bhv="do_joy_B", act="듣기만 해도 행복한 걸?")
        
        # 2.1 문제 해결
        pibo = cm.tts(bhv="do_joy_A", string="파이보도 이제 기분 좋은 말을 많이 쓰도록 노력해야겠다. 알려줘서 정말 고마워!")
                            
        
        
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
    sol.Badword()