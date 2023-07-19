# -*- coding: utf-8 -*-

# 동화-곰과 두 여행자

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


class Fairytale():    
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = config['user_name'] 
                
        
    def Snowwhite(self):
        
        # 1. 동화 줄거리 대화
        pibo = cm.tts(bhv="do_joy_A", string=f"정말 재미있는 이야기였어! {wm.word(self.user_name, 0)}는 어떤 장면이 재미있었니?")
        answer = cm.responses_proc(re_bhv="do_joy_A", re_q=f"{wm.word(self.user_name, 0)}는 어떤 장면이 재미있었니?",
                                   neu_bhv="do_compliment_S", neu=f"그럴 수 있지.")

        pibo = cm.tts(bhv="do_question_L", string=f"백설 공주를 도와준 일곱 난쟁이 들은 숲 속에서 어떤 일을 할 것 같니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"백설 공주를 도와준 일곱 난쟁이 들은 숲 속에서 어떤 일을 할 것 같니?", 
                                   pos_bhv="do_question_S", pos=f" 사이좋게 일했을까?", 
                                   neu_bhv="do_compliment_S", neu=f"몰라도 괜찮아.", 
                                   act_bhv="do_question_S", act=f" 사이좋게 일했을까?")
        # 사이좋게 일 했을까? 가 대답을 바라고 하는 말인지? 시나리오상 바로 음식 얘기하는데

        pibo = cm.tts(bhv="do_question_S", string=f"백설공주는 일곱 난쟁이 들을 위해 어떤 음식을 만들었을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"백설공주는 일곱 난쟁이 들을 위해 어떤 음식을 만들었을까?", 
                                   pos_bhv="do_question_S", pos=f"그 음식을 만들었겠구나!", 
                                   act_bhv="do_question_S", act=f"그 음식을 만들었겠구나!")

        pibo = cm.tts(bhv="do_question_S", string=f"새 왕비가 건넨 독 사과는 무슨 맛이었을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"새 왕비가 건넨 독 사과는 무슨 맛이었을까?", 
                                   neu_bhv="do_compliment_S", neu=f"모를 수 있지.")

        pibo = cm.tts(bhv="do_question_L", string=f"솔직한 대답을 하는 마법 거울에게 {wm.word(self.user_name, 0)}는 어떤 걸 물어보고 싶니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"솔직한 대답을 하는 마법 거울에게 {wm.word(self.user_name, 0)}는 어떤 걸 물어보고 싶니?")
                
        # 2. 등장인물 공감 대화
        pibo = cm.tts(bhv="do_question_S", string=f"새 왕비를 피해 숲 속으로 도망간 백설 공주는 걱정됐을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"새 왕비를 피해 숲 속으로 도망간 백설 공주는 걱정됐을까?", 
                                   pos_bhv="do_question_S", pos=f"{wm.word(self.user_name, 0)}도 최근에 걱정했던 일이 있니?", 
                                   act_bhv="do_question_S", act=f"{wm.word(self.user_name, 0)}도 최근에 걱정했던 일이 있니?")

        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}도 최근에 걱정했던 일이 있니?",
                                       pos_bhv="do_compliment_S", pos=f"그런일이 있었구나!", 
                                       act_bhv="do_compliment_S", act=f"그런일이 있었구나!")

        pibo = cm.tts(bhv="do_question_L", string=f"독사과를 먹고 잠들어 버린 백설 공주를 보는 난쟁이 들은 너무 슬펐겠지?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"독사과를 먹고 잠들어 버린 백설 공주를 보는 난쟁이 들은 너무 슬펐겠지?", 
                                   pos_bhv="do_question_L", pos=f"{wm.word(self.user_name, 0)}도 슬펐던 적이 있다면 이야기해 줄래?", 
                                   act_bhv="do_question_L", act=f"{wm.word(self.user_name, 0)}도 슬펐던 적이 있다면 이야기해 줄래?")

        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}도 슬펐던 적이 있다면 이야기해 줄래?", 
                                       pos_bhv="do_compliment_S", pos=f" 그런 일이 있었구나!", 
                                       act_bhv="do_compliment_S", act=f" 그런 일이 있었구나!")


        # 3. 마무리 대화
        pibo = cm.tts(bhv="do_question_L", string=f"백설 공주를 잘 돌봐준 난쟁이들을 칭찬해볼까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"백설 공주를 잘 돌봐준 난쟁이들을 칭찬해볼까?",  
                                   pos_bhv="do_compliment_S", pos=f"그렇구나!",
                                   neu_bhv="do_compliment_S", neu=f"괜찮아. 모를 수 있지.",
                                   neg_bhv="do_compliment_S", neg=f"그렇구나!",
                                   act_bhv="do_compliment_S", act=f"그렇구나!")
        
        pibo = cm.tts(bhv="do_explain_C", string=f"다음에 또 재미있는 동화를 들려줄게.")
            
        


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
    
    fat = Fairytale()
    fat.Snowwhite()