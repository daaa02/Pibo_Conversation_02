# -*- coding: utf-8 -*-

# 동화-여우와 나무꾼

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
        self.story_name = '여우와나무꾼'
        self.score = []
        self.turns = []
        self.reject = []
        
    def Fox(self):
        
        # 0. 동화 읽어주기
        pibo = cm.tts(bhv="do_breath1", string=f"내가 재미있는 이야기를 들려 줄게. 동화 제목은 {wm.word(self.story_name, 0)}야.")
        f = open('/home/pi/Pibo_Conversation/src/Fairytale/data/10_fox_story.txt', 'r')
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
        
        pibo = cm.tts(bhv="do_question_L", string=f"나무꾼에게 도움을 청한 여우를 왜 숨겨주었다고 생각하니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"나무꾼에게 도움을 청한 여우를 왜 숨겨주었다고 생각하니?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])  

        pibo = cm.tts(bhv="do_question_L", string=f"나무꾼이 여우를 숨겨주지 않았다면 어떤 일이 일어났을까? ")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"나무꾼이 여우를 숨겨주지 않았다면 어떤 일이 일어났을까? ", 
                                   pos_bhv="do_compliment_S", pos=f"그랬겠구나! ", 
                                   neu_bhv="do_compliment_S", neu=f"몰라도 괜찮아.", 
                                   act_bhv="do_compliment_S", act=f"그랬겠구나! ")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])  

        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}도 숨바꼭질 같이 숨는 놀이를 해본 적이 있다면 이야기해줄래?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}도 숨바꼭질 같이 숨는 놀이를 해본 적이 있다면 이야기해줄래?", 
                                   pos_bhv="do_compliment_S", pos=f"재밌었니?", 
                                   neu_bhv="do_compliment_S", neu=f"괜찮아. 대답하기 어려울 수 있어.", 
                                   act_bhv="do_compliment_S", act=f"재밌었니?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])  

        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}도 숨바꼭질 같이 숨는 놀이를 해본 적이 있다면 이야기해줄래?", 
                                       pos_bhv="do_question_S", pos=f"그랬구나!", 
                                       act_bhv="do_question_S", act=f"그랬구나!")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])  

        # 2. 등장인물 공감 대화
        pibo = cm.tts(bhv="do_question_S", string=f"사냥꾼과 사냥개 에게 쫓기고 있던 여우의 마음은 무서웠을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"사냥꾼과 사냥개 에게 쫓기고 있던 여우의 마음은 무서웠을까?", 
                                   pos_bhv="do_question_S", pos=f"{wm.word(self.user_name, 0)}는 무서웠던 적이 있니?", 
                                   neu_bhv="do_compliment_S", neu=f"모를 수 있지.",
                                   act_bhv="do_question_S", act=f"{wm.word(self.user_name, 0)}는 무서웠던 적이 있니?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])  

        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 무서웠던 적이 있니?", 
                                       pos_bhv="do_compliment_S", pos=f"그런일이 있었구나!", 
                                       act_bhv="do_compliment_S", act=f"그런일이 있었구나!")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])  

        pibo = cm.tts(bhv="do_question_L", string=f"잘 숨겨준 줄 알았던 나무꾼의 손짓을 보며 여우는 나무꾼이 미웠을까? ")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"잘 숨겨준 줄 알았던 나무꾼의 손짓을 보며 여우는 나무꾼이 미웠을까? ", 
                                   pos_bhv="do_question_L", pos=f"{wm.word(self.user_name, 0)}도 믿었지만 속상한 경험이 있었다면 이야기해 줄래?",
                                   act_bhv="do_question_L", act=f"{wm.word(self.user_name, 0)}도 믿었지만 속상한 경험이 있었다면 이야기해 줄래?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])  

        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}도 믿었지만 속상한 경험이 있었다면 이야기해 줄래?", 
                                       pos_bhv="do_compliment_S", pos=f"그런 일이 있었구나!", 
                                       act_bhv="do_compliment_S", act=f"그런 일이 있었구나!")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])  


        # 3. 마무리 대화
        pibo = cm.tts(bhv="do_question_L", string=f"만약 {wm.word(self.user_name, 0)}가 여우를 속인 나무꾼을 만난다면 뭐라고 해줄 수 있을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"만약 {wm.word(self.user_name, 0)}가 여우를 속인 나무꾼을 만난다면 뭐라고 해줄 수 있을까?",  
                                   pos_bhv="do_compliment_S", pos=f"그렇구나!",
                                   neu_bhv="do_compliment_S", neu=f"괜찮아. 대답하기 어려울 수 있어. ",
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
    fat.Fox()