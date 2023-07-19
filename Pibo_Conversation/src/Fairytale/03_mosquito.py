# -*- coding: utf-8 -*-

# 동화-모기와 사자

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
        self.story_name = '모기와 사자'
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = config['user_name'] 
        
    
    def Mosqutio(self):      
        
        # 0. 동화 읽어주기
        pibo = cm.tts(bhv="do_breath1", string=f"내가 재미있는 이야기를 들려 줄게. 동화 제목은 {wm.word(self.story_name, 0)}야.")
        f = open('/home/pi/Pibo_Package_02/Pibo_Conversation/src/Fairytale/data/03_mosquito_story.txt', 'r')
        lines = f.readlines()
        # print(lines)
        
        for i in range(0, len(lines), 2):
            try:
                pibo = cm.tts(bhv="", voice="nara", string=f"{lines[i]}")
                pibo = cm.tts(bhv="", voice="ndain", string=f"{lines[i+1]}")
            except IndexError as e:
                break
        
        # 1. 동화 줄거리 대화  
        pibo = cm.tts(bhv="do_joy_A", string=f"정말 재미있는 이야기였어! {wm.word(self.user_name, 0)}는 어떤 장면이 재미있었니?")
        answer = cm.responses_proc(re_bhv="do_joy_A", re_q=f"{wm.word(self.user_name, 0)}는 어떤 장면이 재미있었니?",
                                   neu_bhv="do_compliment_S", neu=f"그럴 수 있지.")
        
        # 2. 등장인물 공감 대화        
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 언제 모기에 물렸었니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 언제 모기에 물렸었니?", 
                                   neu_bhv="do_compliment_S", neu=f"모를 수 있지.")
        
        pibo = cm.tts(bhv="do_question_S", string=f"모기한테 물린 사자 얼굴은 어떻게 변했을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"모기한테 물린 사자 얼굴은 어떻게 변했을까?", 
                                   neu_bhv="do_compliment_S", neu=f"몰라도 괜찮아.")
        
        pibo = cm.tts(bhv="do_question_S", string=f"만약 사자가 거미줄에 걸린 모기를 본다면 구해줄까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"만약 사자가 거미줄에 걸린 모기를 본다면 구해줄까?", 
                                   pos_bhv="do_compliment_S", pos=f"사자는 그럴 수 있겠구나..",
                                   neg_bhv="do_compliment_S", neg=f"사자는 그럴 수 있겠구나..",
                                   act_bhv="do_compliment_S", act=f"사자는 그럴 수 있겠구나..")
            
        pibo = cm.tts(bhv="do_question_L", string=f"거미줄에 걸린 모기는 움직일 수 없었을 때 무서웠을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"거미줄에 걸린 모기는 움직일 수 없었을 때 무서웠을까?", 
                                   pos_bhv="do_question_L", pos=f"최근에 무섭다고 느낀 일이 있다면 말해줄래?")
        
        if answer[0][0] == "positive": 
            answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"최근에 무섭 느낀 일이 있다면 말해줄래?", 
                                       pos_bhv="do_compliment_S", pos=f"정말 무서웠겠는걸?", 
                                       act_bhv="do_compliment_S", act=f"정말 무서웠겠는걸?")
            
        pibo = cm.tts(bhv="do_question_S", string=f"모기가 큰 사자랑 싸워서 이겼을 때는 기뻤을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"모기가 큰 사자랑 싸워서 이겼을 때는 기뻤을까?", 
                                   pos_bhv="do_question_L", pos=f"최근에 놀이에서 이겨 기뻤던 적이 있으면 이야기해 줄래?")
        
        if answer[0][0] == "positive": 
            answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"최근에 놀이에서 이겨 기뻤던 적이 있으면 이야기해 줄래?", 
                                       pos_bhv="do_compliment_S", pos=f"그런 일이 있었구나!", 
                                       act_bhv="do_compliment_S", act=f"그런 일이 있었구나!")

        # 3. 마무리 대화
        pibo = cm.tts(bhv="do_suggestion_L", string=f"만약 {wm.word(self.user_name, 0)}가 자신만만한 모기를 만난다면 뭐라고 해줄 수 있을까?")
        answer = cm.responses_proc(re_bhv="do_suggestion_L", re_q=f"{wm.word(self.user_name, 0)}가 자신만만한 모기를 만난다면 뭐라고 해줄 수 있을까?", 
                                   pos_bhv="do_compliment_S", pos=f"{wm.word(self.user_name, 0)}는 그렇게 말해주고 싶구나!", 
                                   neu_bhv="do_compliment_S", neu=f"괜찮아. 모를 수 있지.", 
                                   act_bhv="do_compliment_S", act=f"{wm.word(self.user_name, 0)}는 그렇게 말해주고 싶구나!")
        
        pibo = cm.tts(bhv="do_explain_C", string=f"다음에 또 재미있는 동화 들려줄게.")
            

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
    fat.Mosqutio()
