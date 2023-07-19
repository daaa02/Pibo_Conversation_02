# -*- coding: utf-8 -*-

# 문제해결-남의 것을 함부로 손대면 안 돼

import os, sys
import re
import csv
import random
from datetime import datetime
import time
import json

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
                
        
    def Other(self):
        
        # 1.1 문제 제시
        pibo = cm.tts(bhv="do_sad", string="자꾸 다른 친구 물건이 예뻐 보이고 갖고 싶어. ")
        
        # 1.2 경험 질문
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 다른 친구 물건이 갖고 싶거나 만져보고 싶을 때가 있었니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}도 잘 몰라서 속상했던 적이 있니?는 다른 친구 물건이 갖고 싶거나 만져보고 싶을 때가 있었니?",
                                   pos_bhv="do_question_S", pos="어떤 물건이었는지 기억이 나니?")                

        if answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="어떤 물건이었는지 기억이 나니?",
                                       neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어.")

        pibo = cm.tts(bhv="do_question_S", string="다른 친구 물건이 예뻐 보여서 갖고 싶을 땐 어떻게 하는 게 좋을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="다른 친구 물건이 예뻐 보여서 갖고 싶을 땐 어떻게 하는 게 좋을까?",
                                   pos_bhv="do_compliment_S", pos="그렇게 생각하는구나!",
                                   neu_bhv="do_explain_C", neu="괜찮아. 모를 수도 있어.",
                                   act_bhv="do_compliment_S", act="그렇게 생각하는구나!")
        
        pibo = cm.tts(bhv="do_question_S", string=f"다른 친구가 {wm.word(self.user_name, 0)} 물건을 함부로 만지면 {wm.word(self.user_name, 0)}는 기분이 어떨까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"다른 친구가 {wm.word(self.user_name, 0)} 물건을 함부로 만지면 {wm.word(self.user_name, 0)}는 기분이 어떨까?",
                                   pos_bhv="do_compliment_S", pos=f"{wm.word(self.user_name, 0)}의 기분이 안 좋겠지?",
                                   neu_bhv="do_explain_B", neu=f"아마 {wm.word(self.user_name, 0)}의 기분이 안 좋겠지?",
                                   neg_bhv="do_compliment_S", neg=f"{wm.word(self.user_name, 0)}의 기분이 안 좋겠지?",
                                   act_bhv="do_compliment_S", act=f"{wm.word(self.user_name, 0)}의 기분이 안 좋겠지?")
        
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}가 친구의 물건을 마음대로 만지면 친구의 기분을 어떨까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}가 친구의 물건을 마음대로 만지면 친구의 기분을 어떨까?",
                                   pos_bhv="do_compliment_S", pos="친구의 기분도 안 좋을 것 같아",
                                   neu_bhv="do_explain_B", neu="괜찮아. 상상하기 어려울 수 있어. 아마 친구의 기분도 안 좋을 것 같아.",
                                   neg_bhv="do_compliment_S", neg="친구의 기분도 안 좋을 것 같아",
                                   act_bhv="do_compliment_S", act="친구의 기분도 안 좋을 것 같아")
        
        pibo = cm.tts(bhv="do_question_S", string="친구의 물건을 만져보고 싶을때는 친구에게 어떻게 이야기 해야 할까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="친구의 물건을 만져보고 싶을때는 친구에게 어떻게 이야기 해야 할까?",
                                   neu_bhv="do_suggestion_S", neu="만져봐도 될까? 라고 말하면 어떨까?")
        
        # 2.1 문제 해결
        pibo = cm.tts(bhv="do_joy_A", string="파이보도 친구들의 물건을 함부로 만지면 안되는 것을 알았어. 알려줘서 정말 고마워!")
                            
        
        
        
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
    sol.Other()