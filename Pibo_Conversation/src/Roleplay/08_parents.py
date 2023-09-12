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
        self.time = 5  # 테스트를 위해 5까지만 셈
        self.role=''
        self.count = 0
        self.score = []
        self.turns = []
        self.reject = []
        
    
    def Parents(self):
        
        # 1. 역할 알림
        pibo = cm.tts(bhv="do_suggestion_S", string="역할 놀이를 해볼까?")
        pibo = cm.tts(bhv="do_suggestion_S", string=f"오늘은 {wm.word(self.user_name, 0)}가 집의 어른이 되어보자!") 
                
        # 2. 역할 놀이 (1 of 3)     # 2개만 있음
        rand = random.sample(range(1,3), 1)
        
        if rand[0] == 1: 
            self.role = "엄마"
            pibo = cm.tts(bhv="do_suggestion_S", string=f"엄마가 되어 {wm.word(self.user_name, 0)}가 장난감 정리를 해보자!")
            pibo = cm.tts(bhv="do_suggestion_S", string=f"내가 5분 줄게. 지금부터 100까지 센다!")
            
            for i in range(1, (self.time+1)):   # 테스트를 위해 10까지만 셈
                text_to_speech(f"{i}")
                time.sleep(2)   # 3초에 1카운트
            
            pibo = cm.tts(bhv="do_waiting_A", string="다 되면 다 됐다고 말해줘!")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="다 되면 다 됐다고 말해줘!",
                                       neu_bhv="do_compliment_S", neu="몰라도 괜찮아.")    # 뭘 모르죠
            
            pibo = cm.tts(bhv="do_joy_A", string="정리를 하고 나니 깨끗해진 것 같아!")
        
        if rand[0] == 2:
            self.role = "아빠"
            pibo = cm.tts(bhv="do_suggestion_S", string=f"아빠가 되어 아빠가 좋아하는 요리를 만들어 보자!")
            pibo = cm.tts(bhv="do_suggestion_S", string=f"내가 3분을 줄게. 지금부터 만들어보자 시작!")
            
            for i in range(1, (self.time+1)):   # 테스트를 위해 10까지만 셈
                text_to_speech(i)
                time.sleep(2)   # 3초에 1카운트
            
            pibo = cm.tts(bhv="do_waiting_A", string="다 되면 다 됐다고 말해줘!")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="다 되면 다 됐다고 말해줘!",
                                       neu_bhv="do_compliment_S", neu="몰라도 괜찮아.")
            
            pibo = cm.tts(bhv="do_joy_A", string="맛있는 냄새가 나는 것 같아!")
        
        # 3. 대화 시작 (3 of 6)     # 4개만 있음
        rand = random.sample(range(1,5), 3)
        
        while True:
            for i in range(len(rand)):
                if rand[i] == 1:                             
                    pibo = cm.tts(bhv="do_sad", string=f"우리 {wm.word(self.role, 2)} 나한테 조용히 하라는 말을 제일 많이 해.")
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.role, 1)} {wm.word(self.user_name, 0)}에게 제일 많이 하는 말은 뭐니?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.role, 1)} {wm.word(self.user_name, 0)}에게 제일 많이 하는 말은 뭐니?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어.",
                                               act_bhv="do_question_S", act=f"그 말을 들을 때 {wm.word(self.user_name, 0)}의 기분은 어떠니?")  
                    
                    if answer[0][0] == "action":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"그 말을 들을 때 {wm.word(self.user_name, 0)}의 기분은 어떠니?",
                                                   neu_bhv="do_compliment_S", neu=f"괜찮아. 대답하기 어려울 수 있어. {wm.word(self.role, 3)}를 흉내내볼까?",
                                                   act_bhv="do_suggestion_S", act=f"{wm.word(self.role, 3)} 흉내내볼까?")
                    
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.role, 3)} 흉내내볼까?")                    
                    self.count += 1 

                if rand[i] == 2:                             
                    pibo = cm.tts(bhv="do_sad", string=f"{wm.word(self.role, 2)} 하는 말 중에 {wm.word(self.user_name, 0)}가 가장 듣기 싫은 말은 뭐니?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.role, 2)} 하는 말 중에 {wm.word(self.user_name, 0)}가 가장 듣기 싫은 말은 뭐니?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 대답하기 어려울 수 있어.",
                                               act_bhv="do_sad", act=f"{wm.word(self.user_name, 0)}가 속상했겠다.")  
                    
                    if answer[0][0] == "action":
                        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.role, 2)} 어떻게 말하면 {wm.word(self.user_name, 0)}가 덜 속상할까?")
                        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.role, 2)} 어떻게 말하면 {wm.word(self.user_name, 0)}가 덜 속상할까?",
                                                   neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어.",
                                                   act_bhv="do_compliment_S", act="그것도 좋은 방법이야!")
                    self.count += 1 
                    
                if rand[i] == 3:                             
                    pibo = cm.tts(bhv="do_sad", string=f"{wm.word(self.user_name, 0)}가 {wm.word(self.role, 0)}에게 가장 화가 났던 때는 언제였어?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.role, 2)} 하는 말 중에 {wm.word(self.user_name, 0)}가 가장 듣기 싫은 말은 뭐니?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 대답하기 어려울 수 있어.",
                                               act_bhv="do_question_S", act="자세히 이야기해 줄래?")  
                    
                    if answer[0][0] == "action":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"자세히 이야기해 줄래?",
                                                   neu_bhv="do_compliment_S", neu="괜찮아. 대답하기 어려울 수 있어.",
                                                   act_bhv="do_compliment_S", act=f"{wm.word(self.user_name, 0)}의 기분이 안 좋았겠다.")
                    self.count += 1 
                      
                if rand[i] == 4:                             
                    pibo = cm.tts(bhv="do_sad", string=f"{wm.word(self.role, 2)} 해준 말 중에 {wm.word(self.user_name, 0)}를 가장 행복하게 하는 말은 뭐니?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.role, 2)} 하는 말 중에 {wm.word(self.user_name, 0)}가 가장 듣기 싫은 말은 뭐니?",
                                               pos_bhv="do_question_S", pos="그 말을 언제 가장 듣고 싶니?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어.",
                                               act_bhv="do_question_S", act="그 말을 언제 가장 듣고 싶니?")  
                    
                    if answer[0][0] == "action" or answer[0][0] == "positive":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"그 말을 언제 가장 듣고 싶니?",
                                                   neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어.",
                                                   act_bhv="do_joy_B", act=" 기분 좋겠는 걸?")
                    self.count += 1 
                            
            if self.count < 3:
                print(self.count)
                continue
            
            elif self.count == 3:
                print(self.count)
                break
        
        # 4. 마무리 대화
        pibo = cm.tts(bhv="do_joy_B", string="오늘 역할놀이도 정말 재미있었어. 다음에 또 놀자!")




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
    rop.Parents()