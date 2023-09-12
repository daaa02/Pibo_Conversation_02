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


class Roleplay():    
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = "예진" 
        self.role=''
        self.count = 0
        self.score = []
        self.turns = []
        self.reject = []
        
    
    def Doctor(self):      # 이 시나리오 미완성인듯
        
        # 1. 역할 알림
        pibo = cm.tts(bhv="do_suggestion_S", string="역할 놀이를 해볼까?")
        pibo = cm.tts(bhv="do_suggestion_S", string=f"오늘은 의사 역할 놀이를 해볼거야.") 
                
        # 2. 역할 놀이
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 언제 병원에 가니?")        
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}는 언제 병원에 가니?",
                                   neu_bhv="do_compliment_S", neu="몰라도 괜찮아.")
        
        pibo = cm.tts(bhv="do_explain_A", string=f"병원은 아픈 사람들을 치료해 주는 곳이야. {wm.word(self.user_name, 0)}가 의사 선생님이 되어서 나를 치료해 줘.")
        
        pibo = cm.tts(bhv="do_suggestion_L", string="안녕하세요. 선생님 머리가 아파서 병원에 왔어요. 머리를 만져 주세요.")     
        answer = cm.responses_proc(re_bhv="do_waiting_A", re_q="머리를 만져 주세요.",
                                   act_bhv="do_question_S", act="의사 선생님, 제 심장 소리는 어떤가요?")
        
        if answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="의사 선생님, 제 심장 소리는 어떤가요?")
      
        pibo = cm.tts(bhv="do_joy_A", string="감사합니다. 선생님께서 진찰해 주셔서 저는 몸이 다 나은 것 같아요.")
        
        pibo = cm.tts(bhv="do_suggestion_L", string=f"이제 파이보가 의사 선생님이 되어서 {wm.word(self.user_name, 0)}의 몸과 마음을 살펴볼게!")
        
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}의 심장은 어디있을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}의 심장은 어디있을까?",
                                   neu_bhv="do_explain_B", neu="몰라도 괜찮아. 가슴 왼쪽을 만져보면 심장이 콩닥콩닥 뛰고 있을거야. 심장이 있는 곳이 마음이 있는 곳이란다!",
                                   act_bhv="do_explain_B", act="가슴 왼쪽을 만져보면 심장이 콩닥콩닥 뛰고 있을거야. 심장이 있는 곳이 마음이 있는 곳이란다!")
            
        # 3. 대화 시작
        pibo = cm.tts(bhv="do_explain_C", string="파이보는 놀이동산에 갔을 때 마음이 가장 행복했던 것 같아.")
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}의 마음이 가장 행복했던 때는 언제였니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}의 마음이 가장 행복했던 때는 언제였니?",
                                   pos_bhv="do_question_S", pos="자세히 말해줄래?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 바로 떠오르지 않을 수 있어",
                                   act_bhv="do_question_S", act="자세히 말해줄래?")
        
        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="자세히 말해줄래?",
                                       pos_bhv="do_joy_A", pos=f"{wm.word(self.user_name, 0)}가 행복했다니 파이보도 기분이 좋아!",
                                       neu_bhv="do_compliment_S", neu="괜찮아. 대답하기 어려울 수도 있어.",
                                       act_bhv="do_joy_A", act=f"{wm.word(self.user_name, 0)}가 행복했다니 파이보도 기분이 좋아!")
            
        pibo = cm.tts(bhv="do_question_S", string=f"그럼 {wm.word(self.user_name, 0)}의 마음이 제일 슬플 때는 언제였니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}의 마음이 가장 행복했던 때는 언제였니?",                                   
                                   neu_bhv="do_compliment_S", neu="괜찮아. 대답하기 어려울 수 있어.",
                                   neg_bhv="do_question_S", neg="무슨 일이 있었니?",
                                   act_bhv="do_question_S", act="무슨 일이 있었니?")
        
        if answer[0][0] == "negative" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="무슨 일이 있었니?",
                                       pos_bhv="do_joy_A", pos=f"{wm.word(self.user_name, 0)}가 속상했겠는걸?",
                                       neu_bhv="do_compliment_S", neu="괜찮아. 대답하기 어려울 수 있어.",
                                       act_bhv="do_joy_A", act=f"{wm.word(self.user_name, 0)}가 속상했겠는걸?")
            
        pibo = cm.tts(bhv="do_explain_C", string="나는 친구들이 내 말을 들어주지 않을 때 제일 화가 났어.")
        
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}의 마음이 제일 화가 날 때는 언제였니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}의 마음이 제일 화가 날 때는 언제였니?",                                   
                                   neu_bhv="do_compliment_S", neu="괜찮아. 대답하기 어려울 수 있어.",
                                   neg_bhv="do_question_S", neg="무슨 일이 있었니?",
                                   act_bhv="do_question_S", act="무슨 일이 있었니?")
        
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}의 마음이 제일 콩닥콩닥 거렸을 때는 언제였니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}의 마음이 제일 콩닥콩닥 거렸을 때는 언제였니?",                                   
                                   neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어",
                                   act_bhv="do_question_S", act="자세히 이야기해 줄래?")
        
        if answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="자세히 이야기해 줄래?",
                                       pos_bhv="do_joy_A", pos="파이보의 마음도 콩닥거리는 걸? ",
                                       neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어.",
                                       act_bhv="do_joy_A", act="파이보의 마음도 콩닥거리는 걸? ")
        
        
        # 4. 마무리 대화
        pibo = cm.tts(bhv="do_joy_B", string=f"{wm.word(self.user_name, 0)}의 마음을 들어볼 수 있어서 좋았어. 다음에도 같이 의사 선생님 놀이 하자! 파이보가 {wm.word(self.user_name, 0)}의 몸과 마음을 살펴줄게.!")




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
    rop.Doctor()