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
        self.story_name = '곰과 두 여행자'
        self.score = []
        self.turns = []
        self.reject = []
        
    def Bear(self):
        
        # 0. 동화 읽어주기
        pibo = cm.tts(bhv="do_breath1", string=f"내가 재미있는 이야기를 들려 줄게. 동화 제목은 {wm.word(self.story_name, 0)}야.")
        f = open('/home/pi/Pibo_Conversation/src/Fairytale/data/08_bear_story.txt', 'r')
        lines = f.readlines()
        # print(lines)
        
        for i in range(0, len(lines), 2):
            try:
                text_to_speech(voice="nara", text=f"{lines[i]}")
                text_to_speech(voice="ndain", text=f"{lines[i+1]}")
            except IndexError as e:
                break
        
        # 1. 동화 줄거리 대화
        pibo = cm.tts(bhv="do_joy_A", string=f"정말 재미있는 이야기였어! {wm.word(self.user_name, 0)}는 어떤 장면이 재미있었니?")
        answer = cm.responses_proc(re_bhv="do_joy_A", re_q=f"{wm.word(self.user_name, 0)}는 어떤 장면이 재미있었니?",
                                   neu_bhv="do_compliment_S", neu=f"그럴 수 있지.")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])  

        pibo = cm.tts(bhv="do_question_S", string=f"두 여행자는 어디를 여행하는 중이었을것 같니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"두 여행자는 어디를 여행하는 중이었을것 같니?", 
                                   pos_bhv="do_question_S", pos=f"여행지에서 무엇을 했을까?", 
                                   act_bhv="do_question_S", act=f"여행지에서 무엇을 했을까?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])  

        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_S", string=f"여행지에서 무엇을 했을까?", 
                                       pos_bhv="do_compliment_S", pos=f"그렇게 생각하는구나!", 
                                       neu_bhv="do_compliment_S", neu=f"모를 수 있지.", 
                                       act_bhv="do_compliment_S", act=f"그렇게 생각하는구나!")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])  

        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}도 최근에 가족들이랑 여행 간 적이 있다면 이야기해줄래?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}도 최근에 가족들이랑 여행 간 적이 있다면 이야기해줄래?", 
                                   pos_bhv="do_question_L", pos=f"{wm.word(self.user_name, 0)}가 너무 좋았을 것 같아! 그 여행은 어땠어?", 
                                   act_bhv="do_question_L", act=f"{wm.word(self.user_name, 0)}가 너무 좋았을 것 같아! 그 여행은 어땠어?") 
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])  

        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_S", strre_qing=f"그 여행은 어땠어?", 
                                       pos_bhv="do_compliment_S", pos=f"그랬구나!", 
                                       neu_bhv="do_compliment_S", neu=f"괜찮아. 모를 수 있지.", 
                                       act_bhv="do_compliment_S", act=f"그랬구나!")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])  

        pibo = cm.tts(bhv="do_question_L", string=f"여행자들처럼 실제로 곰을 본다면 {wm.word(self.user_name, 0)}는 어떻게 할 것 같니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"여행자들처럼 실제로 곰을 본다면 {wm.word(self.user_name, 0)}는 어떻게 할 것 같니?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])  
                
        # 2. 등장인물 공감 대화
        pibo = cm.tts(bhv="do_question_S", string=f"두 여행자가 곰을 만났을 때 놀라고 두려웠을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"두 여행자가 곰을 만났을 때 놀라고 두려웠을까?", 
                                   pos_bhv="do_question_L", pos=f"{wm.word(self.user_name, 0)}는 최근에 놀라고 두려웠던 적이 있니?", 
                                   act_bhv="do_question_L", act=f"{wm.word(self.user_name, 0)}는 최근에 놀라고 두려웠던 적이 있니?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])  

        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}는 최근에 놀라고 두려웠던 적이 있니?", 
                                       pos_bhv="do_compliment_S", pos=f"그랬구나! 정말 무서웠겠다!", 
                                       act_bhv="do_compliment_S", act=f"그랬구나! 정말 무서웠겠다!")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])  

        pibo = cm.tts(bhv="do_question_L", string=f"곰을 만나 자신을 버려두고 도망가는 걸 본 친구의 마음은 속상했을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"곰을 만나 자신을 버려두고 도망가는 걸 본 친구의 마음은 속상했을까?", 
                                   pos_bhv="do_question_L", pos=f"{wm.word(self.user_name, 0)}도 속상했던 적이 있다면 이야기해 줄래?", 
                                   neu_bhv="do_compliment_S", neu=f"몰라도 괜찮아.", 
                                   act_bhv="do_question_L", act=f"{wm.word(self.user_name, 0)}도 속상했던 적이 있다면 이야기해 줄래?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])  

        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}도 속상했던 적이 있다면 이야기해 줄래?", 
                                       pos_bhv="do_compliment_S", pos=f"그런 일이 있었구나!", 
                                       act_bhv="do_compliment_S", act=f"그런 일이 있었구나!")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])  

        # 3. 마무리 대화
        pibo = cm.tts(bhv="do_question_L", string=f"만약 {wm.word(self.user_name, 0)}가 도망간 친구를 만난다면 뭐라고 해줄 수 있을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", string=f"만약 {wm.word(self.user_name, 0)}가 도망간 친구를 만난다면 뭐라고 해줄 수 있을까?",  
                                   pos_bhv="do_compliment_S", pos=f"그렇구나!",
                                   neu_bhv="do_compliment_S", neu=f"괜찮아. 모를 수 있지.",
                                   neg_bhv="do_compliment_S", neg=f"그렇구나!",
                                   act_bhv="do_compliment_S", act=f"그렇구나!")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])  
        

        # 3. 피드백 수집
        time.sleep(1)                   
        pibo = cm.tts(bhv="do_question_S", string="파이보랑 얘기한 거 재미있었어? 재밌었는지, 별로였는지 얘기해줄래?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"파이보랑 얘기한 거 재미있었어?") 
        
        pibo = cm.tts(bhv="do_explain_C", string=f"다음에 또 재미있는 동화 들려줄게.")
        
              
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
    fat.Bear()