# -*- coding: utf-8 -*-

# 역할놀이-부모님

import os, sys
import re
import time
import json
from datetime import datetime 
import random
import csv

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


class Roleplay():    
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = config['user_name'] 
        self.role=''
        self.count = 0
        self.score = []
        self.turns = []
        self.reject = []
        
    
    def Teacher(self):      # 이 시나리오 미완성인듯
        
        # 1. 역할 알림
        pibo = cm.tts(bhv="do_suggestion_S", string="역할 놀이를 해볼까?")
        pibo = cm.tts(bhv="do_suggestion_S", string=f"오늘은 유치원 선생님이 되어 보는거야.") 
                
        # 2. 역할 놀이
        pibo = cm.tts(bhv="do_explain_A", string="파이보가 유치원 선생님이 된다면  아침에 어린이들에게 인사를 하면서 꼭 안아줄거야.")
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}가 유치원 선생님이 된다면 어린이들에게 어떻게 인사를 해주고 싶니?")
        
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}가 유치원 선생님이 된다면 어린이들에게 어떻게 인사를 해주고 싶니?",
                                   pos_bhv="do_question_S", pos="친구들에게 왜 그렇게 인사해 주고 싶니?",
                                   neu_bhv="do_compliment_S", neu="몰라도 괜찮아.",
                                   act_bhv="do_question_S", act="친구들에게 왜 그렇게 인사해 주고 싶니?")
        
        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_L", re_q="친구들에게 왜 그렇게 인사해 주고 싶니?",
                                       neu_bhv="do_compliment_S", neu="괜찮아. 대답하기 어려울 수 있어.")
        
        # 3. 대화 시작
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}가 유치원 선생님이라면 물건을 뺏는 친구들에게 뭐라고 말해주고 싶니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}가 유치원 선생님이라면 물건을 뺏는 친구들에게 뭐라고 말해주고 싶니?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어.")
        
        pibo = cm.tts(bhv="do_question_L", string="최근에 물건을 뺏는 친구들을 본 적이 있었니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="최근에 물건을 뺏는 친구들을 본 적이 있었니?",
                                   pos_bhv="do_question_S", pos="어떤 상황이었는지 나에게 말해 줄 수 있니?")
        
        if answer[0][0] == "positive":
            pibo = cm.tts(bhv="do_sad", string="어떤 상황이었는지 나에게 말해줄 수 있니? ")
            answer = cm.responses_proc(re_bhv="do_sad", re_q="어떤 상황이었는지 말해줄 수 있니?")
            
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}가 유치원 선생님이라면 싸우고 있는 친구들을 어떻게 화해 시킬 것 같니?")
        
        
        # 4. 마무리 대화
        pibo = cm.tts(bhv="do_joy_B", string=f"{wm.word(self.user_name, 0)}와 유치원 선생님 놀이를 해서 너무 재미있었어. 유치원에서 있었던 다양한 일들을 나에게 또 말해줘!")




        # 3. 피드백 수집
        time.sleep(1)                   
        pibo = cm.tts(bhv="do_question_S", string="파이보랑 얘기한 거 재미있었어? 재밌었는지, 별로였는지 얘기해줄래?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"파이보랑 얘기한 거 재미있었어?")

        pibo = cm.tts(bhv="do_joy_A", string=f"나랑 놀아줘서 고마워.") 
              
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
    
    rop = Roleplay()
    rop.Teacher()