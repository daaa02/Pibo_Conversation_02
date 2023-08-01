# -*- coding: utf-8 -*-

# 문제 해결-아침에 일찍 일어나기 힘들어

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
            self.user_name = config['user_name'] 
        self.score = []
        self.turns = []
        self.reject = []
        
        
    def Morning(self):
        
        # 1.1 문제 제시
        pibo = cm.tts(bhv="do_sad", string="요즘 자꾸 늦잠을 자.")
        
        # 1.2 경험 질문
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, type=0)}도 아침에 일어나기 힘드니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, type=0)}도 아침에 일어나기 힘드니?",
                                   pos_bhv="do_compliment_S", pos="나랑 비슷하구나.")
        
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, type=0)}는 보통 몇시에 일어나니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="보통 몇 시에 일어나니?")
        
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, type=0)} 친구들은 보통 몇시에 일어나는지 알고 있니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, type=0)} 친구들은 보통 몇시에 일어나는지 알고 있니?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 모를 수도 있어.")
        
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, type=0)}랑 친구들 나이에는 일찍자고 일찍 일어나는 것이 좋다고 해!")
        
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, type=0)}는 일어나자마자 하는 일이 있니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, type=0)}는 일어나자마자 하는 일이 있니?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어!")
        
        pibo = cm.tts(bhv="do_question_S", string="어떻게 하면 잠을 빨리 깰 수 있을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="어떻게 하면 잠을 빨리 깰 수 있을까?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 모를 수도 있어.",
                                   act_bhv="do_compliment_S", act="세수를 하는 것도 좋겠지?")
        
        pibo = cm.tts(bhv="do_question_S", string="아침에 일찍 일어나면 뭐가 좋을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="아침에 일찍 일어나면 뭐가 좋을까?",
                                   pos_bhv="do_compliment_S", pos="일찍 일어나면 더 많이 놀 수 있겠지?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 모를 수도 있어.",
                                   act_bhv="do_compliment_S", act="일찍 일어나면 더 많이 놀 수 있겠지?")
        
        # 2.1 마무리 대화
        pibo = cm.tts(bhv="do_joy_A", string="파이보도 이제 일찍 일어나도록 노력해야겠다. 알려줘서 정말 고마워!")
        
        
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
    sol.Morning()