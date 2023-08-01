# -*- coding: utf-8 -*-

# 문제해결-차례를 기다리기 어려워

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
                
        
    def Sequence(self):
        
        # 1.1 문제 제시
        pibo = cm.tts(bhv="do_sad", string="여러 사람들이랑 있을 때 차례를 기다리기가 어려워.")
        
        # 1.2 경험 질문
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}도 차례를 지키는게 어려울 때가 있니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}도 차례를 지키는게 어려울 때가 있니?",
                                   pos_bhv="do_compliment_S", pos="나랑 비슷하구나!",
                                   neg_bhv="do_compliment_S", neg=f"{wm.word(self.user_name, 0)} 대단한 걸?")
            
        pibo = cm.tts(bhv="do_question_L", string="선생님께서 버스에 탈 때는 차례를 지켜야 한다고 했어. 우리는 언제 또 차례를 지켜야 할까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="선생님께서 버스에 탈 때는 차례를 지켜야 한다고 했어. 우리는 언제 또 차례를 지켜야 할까?",
                                   pos_bhv="do_compliment_S", pos="차례를 지켜야 할 때가 많구나!",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 모를 수도 있어.",
                                   act_bhv="do_compliment_S", act="차례를 지켜야 할 때가 많구나!")
            
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 차례를 지키지 않는 사람을 본 적 있니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 차례를 지키지 않는 사람을 본 적 있니?",
                                   pos_bhv="do_compliment_S", pos=f"{wm.word(self.user_name, 0)} 주변에도 있구나!",
                                   neu_bhv="do_compliment_S", neu=f"{wm.word(self.user_name, 0)} 주변 사람들은 차례를 잘 지키는구나!")
            
        pibo = cm.tts(bhv="do_question_S", string="순서를 기다리지 않으면 다른 사람들이 화를 낼까? ")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="순서를 기다리지 않으면 다른 사람들이 화를 낼까? ",
                                   pos_bhv="do_compliment_S", pos="기다리는 사람들은 화가 날 것 같아.",
                                   neu_bhv="do_explain_B", neu="괜찮아. 바로 떠오르지 않을 수 있어. 아마 기다리는 사람들은 화가 나겠지?",
                                   act_bhv="do_compliment_S", act="기다리는 사람들은 화가 날 것 같아.")
        
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 차례를 기다리는 시간이 지루하지는 않니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 차례를 기다리는 시간이 지루하지는 않니?")
        
        pibo = cm.tts(bhv="do_question_L", string="어떻게 하면 기다리는 시간이 빨리 갈까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="어떻게 하면 기다리는 시간이 빨리 갈까?",
                                   pos_bhv="do_compliment_S", pos="또, 노래를 들어도 시간이 빨리가겠다!",
                                   neu_bhv="do_suggestion_S", neu="괜찮아. 생각이 나지 않을 수 있어. 노래를 들으면 시간이 빨리갈 것 같아!",
                                   act_bhv="do_compliment_S", act="또, 노래를 들어도 시간이 빨리가겠다!")
        
        # 2.1 문제 해결
        pibo = cm.tts(bhv="do_joy_A", string="파이보도 이제 차례를 잘 지키도록 노력해야겠다. 알려줘서 정말 고마워!")
                            
        
        
        
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
    sol.Sequence()