# -*- coding: utf-8 -*-

# 일상-자기 전 감정 대화

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


class Daily():    
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = config['user_name'] 
        self.mood = str

    
    def Bedtime(self):
        
        # 1.1 시간 알림
        rand_list = ["벌써 어두운 밤이 되었어.", "하루가 빨리 지나갔지?", "좋은 하루 보냈니?"]
        pibo = cm.tts(bhv="do_explain_A", string=random.choice(rand_list))
        
        # 1.2 점수 파악 . 1.3 대화 시작
        pibo = cm.tts(bhv="do_question_S", string="오늘의 기분을 감정 단어로 말해볼까?")
        pibo = cm.tts(bhv="do_explain_B", string="기분이 좋다면 좋아. 보통이면 평범해. 안 좋았다면 안 좋았어 라고 말할 수 있어!")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="오늘의 기분을 감정 단어로 말해볼까?", 
                                   pos_bhv="do_question_S", pos="오늘 좋은 일이 있다면 말해줄래?",
                                   neu_bhv="do_joy_A", neu=f"오늘 하루도 고생 많았어. 내일은 좋은 일이 가득할거야. {wm.word(self.user_name, type=4)} 잘 자!",
                                   neg_bhv="do_question_S", neg="오늘 무슨 일 있었다면 말해 줄래?",
                                   act_bhv="do_question_S", act="오늘 재미있는 일이 있었다면 말해줄래?")
        
        if answer[0][0] == "positive": self.mood = "좋음"
        if answer[0][0] == "negative": self.mood = "나쁨"
        if answer[0][0] == "action": self.mood = "평범"
        
        if answer[0][0] == "neutral": sys.exit(0)        
    
        answer = cm.responses_proc(re_q="오늘 있었던 일 말해줄 수 있니?",
                                   pos_bhv="do_question_S", pos="어떤 일이 있었니?",
                                   neu_bhv="do_joy_A", neu=f"시간이 벌써 이렇게 됐네! 어서 자야겠는 걸? {wm.word(self.user_name, type=4)} 잘 자!",
                                   neg_bhv="do_joy_A", neg=f"오늘 하루도 고생 많았어. 내일은 좋은 일이 가득할거야. {wm.word(self.user_name, type=4)} 잘 자!",
                                   act_bhv="do_joy_A", act=f"시간이 벌써 이렇게 됐네! 어서 자야겠는 걸? {wm.word(self.user_name, type=4)} 잘 자!")

        if answer[0][0] == "positive":
            if self.mood == "좋음":
                answer = cm.responses_proc(re_bhv="do_question_S", re_q="어떤 일이 있었니?", 
                                           pos_bhv="do_joy_B", pos=f"기분이 좋은 일이었겠는걸?",
                                           act_bhv="do_joy_B", act=f"기분이 좋은 일이었겠는걸?")
            
            if self.mood == "나쁨":
                answer = cm.responses_proc(re_bhv="do_question_S", re_q="어떤 일이 있었니?", 
                                           neg_bhv="do_sad", neg="정말 기분이 안 좋았을 것 같아. 너무 우울해 하지마.",
                                           act_bhv="do_sad", act="정말 기분이 안 좋았을 것 같아. 너무 우울해 하지마.")
            
            if self.mood == "평범":
                answer = cm.responses_proc(re_bhv="do_question_S", re_q="어떤 일이 있었니?",
                                           pos_bhv="do_joy_B", pos="재밌었겠다!",
                                           act_bhv="do_joy_B", act="재밌었겠다!")
            
                
            pibo = cm.tts(bhv="do_joy_A", string=f"활기찬 내일을 위해 오늘은 이만 자자. {wm.word(self.user_name, type=4)} 잘 자!")

        
if __name__ == "__main__":
    day = Daily()
    day.Bedtime()
    