# -*- coding: utf-8 -*-

# 사회기술-어른을 뵈면 공손하게 인사를 드려요

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
from openpibo.vision import Camera
from openpibo.vision import Detect


pibo_camera = Camera()
pibo_detect = Detect()

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


class Etiquette():    
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = config['user_name'] 
        self.correct = ['어른', '인사', '않']
        self.ox = ''
                
        
    def Bow(self):
        
        # 2.1 카드 대화
        pibo = cm.tts(bhv="do_question_L", string="이 카드의 어린이는 무엇을 잘못했을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="이 카드의 어린이는 무엇을 잘못했을까?",
                                   neg_bhv="do_suggestion_S", neg="같이 다시 한번 볼까?",
                                   neu_bhv="do_suggestion_S", neu="같이 다시 한번 볼까?")             
        
        if answer[0][0] == "action":            
            
            for i in range(len(self.correct)):
                if self.correct[i] in answer[0][1]:
                    self.ox = "(right)"                    
            if len(self.ox) == 0:
                self.ox = "(wrong ㅠㅠ)"
              
            if self.ox == "(right)":
                print(self.ox)
                pibo = cm.tts(bhv="do_compliment_S", string="맞아! 아주 똑똑한 걸?")
            else:
                print(self.ox)
                pibo = cm.tts(bhv="do_suggestion_S", string="또 무엇을 잘못했을까?")
                answer = cm.responses_proc(re_bhv="do_suggestion_S", re_q="또 무엇을 잘못했을까?")
                
                if answer[0][0] == "action":        
                                
                    for i in range(len(self.correct)):
                        if self.correct[i] in answer[0][1]:
                            self.ox = "(right)"                    
                    if len(self.ox) == 0:
                        self.ox = "(wrong ㅠㅠ)"
                    
                    if self.ox == "(right)":
                        print(self.ox)
                        pibo = cm.tts(bhv="do_compliment_S", string="맞아! 아주 똑똑한 걸?")
                    else:
                        print(self.ox)
                        pibo = cm.tts(bhv="do_suggestion_S", string="같이 다시 한번 볼까?")
        
        pibo = cm.tts(bhv="do_explain_A", string="이 카드의 어린이는 어른을 보고 인사하지 않았어.")
     
        # 2.2 경험 질문
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 어른들에게 인사를 잘 하니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 어른들에게 인사를 잘 하니?",
                                   pos_bhv="do_joy_A", pos="정말 대단한 걸.?",
                                   neg_bhv="do_question_S", neg="인사를 하기가 쑥스럽니?")
        
        if answer[0] != "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=" 인사를 자주 하다 보면 익숙해 질거야!",     # 이거만 3번 반복할 것 같은데 일단 패스,,
                                       act_bhv="do_compliment_S", act="그럴 수 있지. 인사를 자주 하다 보면 익숙해질 거야!")

        pibo = cm.tts(bhv="do_question_L", string="최근에 어른들을 만나서 인사를 한 적이 있니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="최근에 어른들을 만나서 인사를 한 적이 있니?",
                                   pos_bhv="do_question_S", pos="누구를 만났니?")
        
        if answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="누구를 만났니?",
                                       neu_bhv="do_compliment_S", neu="괜찮아. 기억이 안 날 수도 있지.",
                                       act_bhv="do_question_S", act=f"{wm.word(self.user_name, 0)}는 인사를 어떻게 하니?")
            
            if answer[0][0] == "action":
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name,0)}는 인사를 어떻게 하니?",
                                           neu_bhv="do_explain_A", neu="몰라도 괜찮아. 파이보가 알려줄게!")
        
        # 2.3 문제 인식
        pibo = cm.tts(bhv="do_question_L", string="어른들을 보고도 인사를 하지 않으면 어른들은 어떻게 생각할까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="어른들을 보고도 인사를 하지 않으면 어른들은 어떻게 생각할까?",
                                   pos_bhv="do_compliment_S", pos="예의가 없다고 생각할 수 있겠지? ",
                                   neu_bhv="do_explain_B", neu="괜찮아. 모를 수도. 예의가 없다고 생각할 수 있겠지? ",
                                   act_bhv="do_compliment_S", act="예의가 없다고 생각할 수 있겠지? ")
    
        # 3.1 마무리 대화
        pibo = cm.tts(bhv="do_joy_A", string="어른들을 만났을 땐 안녕하세요. 하고 존댓말로 예의를 갖춰 인사를 하는 거야. 잘 기억해 두자!")
    
        
        
        
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
    
    etq = Etiquette()
    etq.Bow()