# -*- coding: utf-8 -*-

# 사회기술-친구집에서 놀고 난 후에는 정리해요

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
today = datetime.now().strftime('%m%d_%H%M')
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
        self.correct = ['장난감', '정리']
        self.ox = ''
                
        
    def Friend5(self):
        
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
        
        pibo = cm.tts(bhv="do_explain_A", string="이 카드의 어린이는 친구 집에서 같이 놀고 장난감을 정리하지 않았어.")
     
        # 2.2 경험 질문
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 친구 집에서 놀았던 적이 있니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}는 친구 집에서 놀았던 적이 있니?",
                                   pos_bhv="do_question_S", pos="누구와 함께 가서 놀았니?")
        
        if answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="누구와 함께 가서 놀았니?",
                                       neu_bhv="do_compliment_S", neu="기억이 안 날 수 있지. 어떤 장난감을 가지고 놀았니?",
                                       act_bhv="do_question_S", act="어떤 장난감을 가지고 놀았니?")
            
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="어떤 장난감을 가지고 놀았니?",
                                       neu_bhv="do_compliment_S", neu="기억이 안 날 수 있지.")
            
            pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 장난감을 가지고 논 뒤에 정리를 잘 하니?")
            answer = cm.responses_proc(re_bhv="do_question_L", re_q="친구 집에서 늦게 까지 놀면 집에서 엄마가 기다리시겠지?",
                                       pos_bhv="do_explain_A", pos="자기가 가지고 논 장난감은 스스로 정리하는 것이 맞아.",
                                       neu_bhv="do_explain_A", neu="자기가 가지고 논 장난감이라면 스스로 정리하는 것이 맞아.",
                                       act_bhv="do_explain_A", act="자기가 가지고 논 장난감은 스스로 정리하는 것이 맞아.")
                    
        # 2.3 문제 인식
        pibo = cm.tts(bhv="do_question_L", string="놀고 난 뒤 친구 혼자서 많은 장난감을 정리하려면 힘들겠지?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="놀고 난 뒤 친구 혼자서 많은 장난감을 정리하려면 힘들겠지?",
                                   pos_bhv="do_explain_C", pos="너무 힘들어서 다음에는 초대하지 않을지도 몰라.",
                                   neu_bhv="do_explain_C", neu="괜찮아. 모를 수도 있어. 잠을 자야 하는데 너무 힘들어서 다음에는 초대하지 않을지도 몰라.",
                                   act_bhv="do_explain_C", act="너무 힘들어서 다음에는 초대하지 않을지도 몰라.")
    
        # 3.1 마무리 대화
        pibo = cm.tts(bhv="do_joy_A", string="친구네 집에 가서 재밌게 놀고 난 뒤에는 정리하는 것을 도와줘야 해. 꼭 기억해!")
    
        
        
        
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
    
    etq = Etiquette()
    etq.Friend5()