# -*- coding: utf-8 -*-

# 동화-소금 장수와 당나귀

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
        self.story_name = '소금장수와당나귀'
        self.score = []
        self.turns = []
        self.reject = []
        
        
    def Salt(self):
        
        # 0. 동화 읽어주기
        pibo = cm.tts(bhv="do_breath1", string=f"내가 재미있는 이야기를 들려 줄게. 동화 제목은 {wm.word(self.story_name, 0)}야.")
        f = open('/home/pi/Pibo_Conversation/src/Fairytale/data/02_salt_story.txt', 'r')
        lines = f.readlines()
        # print(lines)
        
        for i in range(0, len(lines), 1):
            try:
                text_to_speech(voice="nara", text=f"{lines[i]}")
            except IndexError as e:
                break
        
        # 1. 동화 줄거리 대화
        time.sleep(1)
        pibo = cm.tts(bhv="do_joy_A", string=f"정말 재미있는 이야기였어! {wm.word(self.user_name, 0)}는 어떤 장면이 재미있었니?")
        answer = cm.responses_proc(re_bhv="do_joy_A", re_q=f"{wm.word(self.user_name, 0)}는 어떤 장면이 재미있었니?",
                                   neu_bhv="do_compliment_S", neu=f"그럴 수 있지.")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])  
        
        pibo = cm.tts(bhv="do_question_L", string=f"동화 속 소금 장수와 당나귀는 어디를 가는 길이었을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"동화 속 소금 장수와 당나귀는 어디를 가는 길이었을까?", 
                                   neu_bhv="do_compliment_S", neu=f"모를 수 있지.")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])  

        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}도 유치원 갈 때 가방을 매고 가니? ")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}도 유치원 갈 때 가방을 매고 가니? ", 
                                   pos_bhv="do_question_S", pos=f"{wm.word(self.user_name, 0)} 가방 안에 어떤 것들이 들어있니?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])  
        
        if answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)} 가방 안에 어떤 것들이 들어있니?")
                
            pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}가 말한 것들 말고 유치원에 가져 가고 싶은 물건이 있다면 말해줄래?")
            answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}가 말한 것들 말고 유치원에 가져 가고 싶은 물건이 있다면 말해줄래?", 
                                    pos_bhv="do_question_S", pos=f"그거 가지고 유치원에 가서 뭐하고 싶어?", 
                                    neu_bhv="do_compliment_S", neu=f"몰라도 괜찮아.", 
                                    act_bhv="do_question_S", act=f"그거 가지고 유치원에 가서 뭐하고 싶어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])  

        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"그거 가지고 유치원에 가서 뭐하고 싶어?")   
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])           
        
        # 2. 등장인물 공감 대화
        pibo = cm.tts(bhv="do_question_L", string=f"소금 장수는 당나귀에게 속았다고 생각했을 때 소금 장수는 짜증 났을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"소금 장수는 당나귀에게 속았다고 생각했을 때 소금 장수는 짜증 났을까?", 
                                   pos_bhv="do_question_L", pos=f"{wm.word(self.user_name, 0)}도 누가 {wm.word(self.user_name, 0)}를 속여서 짜증났던 적이 있다면 이야기해 줄래?", 
                                   act_bhv="do_question_L", act=f"{wm.word(self.user_name, 0)}도 누가 {wm.word(self.user_name, 0)}를 속여서 짜증났던 적이 있다면 이야기해 줄래?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])  

        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_L ", re_q=f"{wm.word(self.user_name, 0)}도 누가 {wm.word(self.user_name, 0)}를 속여서 짜증났던 적이 있다면 이야기해 줄래?", 
                                       act_bhv="do_compliment_S", act=f"그런 일이 있었구나! 정말 짜증났었겠다! ")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])  

        pibo = cm.tts(bhv="do_question_L", string=f"당나귀가 꾀를 부려 짐이 훨씬 더 무거워 졌을 때 당나귀는 후회했겠지?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"당나귀가 꾀를 부려 짐이 훨씬 더 무거워 졌을 때 당나귀는 후회했겠지?", 
                                   pos_bhv="do_question_S", pos=f"{wm.word(self.user_name, 0)}도 후회 했던 적이 있었다면 이야기해 줄래?", 
                                   act_bhv="do_question_S", act=f"{wm.word(self.user_name, 0)}도 후회 했던 적이 있었다면 이야기해 줄래?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])  

        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}도 후회 했던 적이 있었다면 이야기해 줄래?", 
                                       act_bhv="do_sad", act=f"그런 일이 있었구나! 정말 속상했겠다!")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])  

        # 3. 마무리 대화
        pibo = cm.tts(bhv="do_suggestion_L", string=f"만약 {wm.word(self.user_name, 0)}가 게으름 피우는 당나귀를 만난다면 뭐라고 해줄 수 있을까?")
        answer = cm.responses_proc(re_bhv="do_suggestion_L", re_q=f"만약 {wm.word(self.user_name, 0)}가 게으름 피우는 당나귀를 만난다면 뭐라고 해줄 수 있을까?", 
                                   pos_bhv="do_compliment_S", pos=f"{wm.word(self.user_name, 0)}는 그렇게 말해주고 싶구나!", 
                                   neu_bhv="do_compliment_S", neu=f"괜찮아. 모를 수 있지.", 
                                   neg_bhv="do_compliment_S", neg=f"{wm.word(self.user_name, 0)}는 그렇게 말해주고 싶구나!", 
                                   act_bhv="do_compliment_S", act=f"{wm.word(self.user_name, 0)}는 그렇게 말해주고 싶구나!")
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
    fat.Salt()