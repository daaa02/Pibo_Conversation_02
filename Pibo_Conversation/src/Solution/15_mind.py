# -*- coding: utf-8 -*-

# 문제해결-속마음을 말하기가 어려워

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
                
        
    def Mind(self):
        
        # 1.1 문제 제시
        pibo = cm.tts(bhv="do_sad", string="파이보는 다른 사람한테 속마음을 말하기가 어려워.")
        
        # 1.2 경험 질문
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}의 속마음을 다른 사람에게 말한 적 있니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}의 속마음을 다른 사람에게 말한 적 있니?",
                                   pos_bhv="do_question_S", pos="말하고 나니까 기분이 어땠니?")                
    
        if answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="말하고 나니까 기분이 어땠니?",
                                       pos_bhv="do_compliment_S", pos="속마음을 말하면 마음이 편해질수도 있겠지?",
                                       act_bhv="do_compliment_S", act="속마음을 말하면 마음이 편해질수도 있겠지?")
            

        pibo = cm.tts(bhv="do_question_L", string=f"나는 속마음이 10개정도 있는 것 같아. {wm.word(self.user_name, 0)}는 속마음이 얼마나 많니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"나는 속마음이 10개정도 있는 것 같아. {wm.word(self.user_name, 0)}는 속마음이 얼마나 많니?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 바로 떠오르지 않을 수 있어.")
        
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}도 속마음을 말하기 어려울 때가 있니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}도 속마음을 말하기 어려울 때가 있니?",
                                   pos_bhv="do_compliment_S", pos=f"나는 속마음을 말로 표현하기 어려운 것 같아. {wm.word(self.user_name, 0)}는 언제 말하기가 어렵니?",
                                   neg_bhv="do_compliment_S", neg=f"파이보는 잘 못하는데, {wm.word(self.user_name, 0)} 정말 대단한 걸?")
        
        if answer[0][0] =="positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"나는 속마음을 말로 표현하기 어려운 것 같아. {wm.word(self.user_name, 0)}는 언제 말하기가 어렵니?",
                                       neu_bhv="do_compliment_S", neu="괜찮아. 대답하기 어려울 수 있어.")
        
        pibo = cm.tts(bhv="do_question_L", string="속마음을 계속 말하지 않으면 어떻게 될까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}가 친구의 물건을 마음대로 만지면 친구의 기분을 어떨까?",
                                   pos_bhv="do_compliment_S", pos="마음이 힘들어 지겠지?",
                                   neg_bhv="do_compliment_S", neg="마음이 힘들어 지겠지?",
                                   act_bhv="do_compliment_S", act="마음이 힘들어 지겠지?")
        
        pibo = cm.tts(bhv="do_question_S", string="나의 속마음을 언제 이야기하는 것이 좋을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="나의 속마음을 언제 이야기하는 것이 좋을까?",
                                   pos_bhv="do_compliment_S", pos="그렇게 생각하는구나!",                                   
                                   neu_bhv="do_suggestion_S", neu="괜찮아. 모를 수도 있어.  속상한 날에는 나에게 꼭 말해줘.",
                                   neg_bhv="do_compliment_S", neg="그렇게 생각하는구나!",
                                   act_bhv="do_compliment_S", act="그렇게 생각하는구나!")
        
        # 2.1 문제 해결
        pibo = cm.tts(bhv="do_joy_A", string="파이보도 이제 속마음을 잘 표현할 수 있도록 노력해야겠다. 알려줘서 정말 고마워!")
                            
        
        
        
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
    sol.Mind()