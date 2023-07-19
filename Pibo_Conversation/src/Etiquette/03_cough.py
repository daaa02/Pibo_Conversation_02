# -*- coding: utf-8 -*-

# 사회기술-입을 가리고 기침을 해요

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
today_start = datetime.now().strftime('%y%m%d_%H%M')
csv_conversation = open(f'{folder}/{today_start}_{filename}.csv', 'a', newline='', encoding = 'utf-8')
csv_preference = open(f'{folder}/aa.csv', 'a', newline='', encoding = 'utf-8')
cwc = csv.writer(csv_conversation)
cwp = csv.writer(csv_preference)
crc = csv.reader(csv_conversation, delimiter=',', doublequote=True, lineterminator='\r\n', quotechar='"')


class Etiquette():    
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = config['user_name'] 
        self.correct = ['기침', '재채기']
        self.ox = ''
        self.score = []
        self.turns = []
        self.reject = []
                
        
    def Cough(self):
        gss.write_sheet(name=self.user_name, today=today_start, activities=filename)
        
        cm.tts(bhv="do_suggestion_L", string=f"2번 카드를 파이보에게 보여줘!")
        
        while True:         
            time.sleep(2)
            img = pibo_camera.read()
            qr = pibo_detect.detect_qr(img)
            self.card_msg = qr['data']
            
            if self.card_msg == "입을 가리고 기침을 해요":
                break
            else:
                cm.tts(bhv="do_suggestion_L", string=f"2번 카드를 다시 보여줄래?")
                continue
        
        # 2.1 카드 대화
        time.sleep(2)
            
        pibo = cm.tts(bhv="do_question_L", string="이 카드의 어린이는 무엇을 잘못했을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="이 카드의 어린이는 무엇을 잘못했을까?",
                                   neg_bhv="do_suggestion_S", neg="같이 다시 한번 볼까?",
                                   neu_bhv="do_suggestion_S", neu="같이 다시 한번 볼까?")    
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])           
        
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
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])  
                
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
        
        pibo = cm.tts(bhv="do_explain_A", string="이 카드의 어린이는 입을 가리지 않고 기침을 했어.")
     
        # 2.2 경험 질문
        pibo = cm.tts(bhv="do_question_L", string="우리는 보통 언제 기침을 할까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="우리는 보통 언제 기침을 할까?",
                                   pos_bhv="do_compliment_S", pos="감기에 걸리면 기침을 하지?",
                                   neu_bhv="do_explain_B", neu="괜찮아 생각이 안 날 수도 있어. 감기에 걸리면 기침을 하지? ",
                                   act_bhv="do_compliment_S", act="감기에 걸리면 기침을 하지?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
        
        
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 밖에서 기침이 나올 때 어떻게 하니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}는 밖에서 기침이 나올 때 어떻게 하니?",
                                   neu_bhv="do_explain_C", neu="괜찮아 모를 수도 있어.")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
        
        pibo = cm.tts(bhv="do_question_L", string="입을 가리지 않고 기침을 하면 어떤 일이 일어날까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="입을 가리지 않고 기침을 하면 어떤 일이 일어날까?",
                                   pos_bhv="do_compliment_S", pos="다른 사람도 감기에 걸릴 수 있겠지?",
                                   neu_bhv="do_explain_B", neu="괜찮아 모를 수도 있어. 다른 사람도 감기에 걸릴 수 있을거야.",
                                   act_bhv="do_compliment_S", act="다른 사람도 감기에 걸릴 수 있겠지?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
        
        # 2.3 문제 인식
        pibo = cm.tts(bhv="do_question_L", string="입을 가리지 않고 기침을 하면 다른 사람들이 어떻게 생각할까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="입을 가리지 않고 기침을 하면 다른 사람들이 어떻게 생각할까?",
                                   pos_bhv="do_compliment_S", pos="다른 사람들은 침이 튀어서 깨끗하지 못하다고 생각하겠지?",
                                   neu_bhv="do_explain_A", neu="괜찮아 모를 수도 있어. 아마 다른 사람들은 침이 튀어서 깨끗하지 않다고 생각할거야.",
                                   act_bhv="do_compliment_S", act="다른 사람들은 침이 튀어서 깨끗하지 못하다고 생각하겠지?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
        
        # 3.1 마무리 대화
        pibo = cm.tts(bhv="do_joy_A", string="기침을 할 때 입을 가리는 건 중요한 공공예절이야. 잘 기억해 두자!")
                            
        
        
        
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
        
        cwp.writerow([today_start, filename, self.score[0], self.score[1], self.score[2],self.score[3]])

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
        today_end = datetime.now().strftime('%y%m%d_%H%M')        
        gss.write_sheet(name=self.user_name, today=today_end, activities=filename)
        




if __name__ == "__main__":
    
    etq = Etiquette()
    etq.Cough()