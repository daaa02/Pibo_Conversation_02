# -*- coding: utf-8 -*-

# 동화-개미와 베짱이

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
today = datetime.now().strftime('%m%d_%H%M')
csv_conversation = open(f'{folder}/{today}_{filename}.csv', 'a', newline='', encoding = 'utf-8')
csv_preference = open(f'{folder}/aa.csv', 'a', newline='', encoding = 'utf-8')
cwc = csv.writer(csv_conversation)
cwp = csv.writer(csv_preference)
crc = csv.reader(csv_conversation, delimiter=',', doublequote=True, lineterminator='\r\n', quotechar='"')


class Fairytale():
        
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = "예진" 
        
    
    def Ants(self):      
        # 1. 동화 줄거리 대화  
        pibo = cm.tts(bhv="do_joy_A", string=f"정말 재미있는 이야기였어! {wm.word(self.user_name, 0)}는 어떤 장면이 재미있었니?")
        answer = cm.responses_proc(re_bhv="do_joy_A", re_q=f"{wm.word(self.user_name, 0)}는 어떤 장면이 재미있었니?",
                                   neu_bhv="do_compliment_S", neu=f"그럴 수 있지.")
             
        pibo = cm.tts(bhv="do_question_S", string=f"개미들은 겨울을 준비하기 위해 어떤 일을 했을 것 같니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"개미들은 겨울을 준비하기 위해 어떤 일을 했을 것 같니?", 
                                   neu_bhv="do_compliment_S", neu=f"모를 수 있지.")
        
        pibo = cm.tts(bhv="do_question_S", string=f"개미들은 어떤 먹이를 모았을 것 같니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"개미들은 어떤 먹이를 모았을 것 같니?", 
                                   neu_bhv="do_compliment_S", neu=f"몰라도 괜찮아.")
        
        pibo = cm.tts(bhv="do_question_L", string=f"베짱이는 좋아하는 노래를 부르며 놀았을 것 같아! {wm.word(self.user_name, 0)}가 좋아하는 노래는 어떤 노래니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}가 좋아하는 노래는 어떤 노래니?", 
                                   pos_bhv="do_compliment_S", pos=f"그 노래를 좋아하는구나!")
            
        # 2. 등장인물 공감 대화   
        pibo = cm.tts(bhv="do_question_S", string=f"추운 겨울 먹을 것이 없던 베짱이는 후회했을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"추운 겨울 먹을 것이 없던 베짱이는 후회했을까?", 
                                   pos_bhv="do_question_S", pos=f"{wm.word(self.user_name, 0)}이도 후회한 적이 있다면 말해줄래?",
                                   neu_bhv="do_compliment_S", neu=f"몰라도 괜찮아.",
                                   neg_bhv="do_question_S", neg=f"{wm.word(self.user_name, 0)}도 후회한 적이 있다면 말해줄래?",
                                   act_bhv="do_question_S", act=f"{wm.word(self.user_name, 0)}도 후회한 적이 있다면 말해줄래?")
        
        if answer[0] != "neutral": 
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}이도 후회한 적이 있다면 말해줄래?")
            
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}가 개미라면 겨울에 베짱이에게 먹을 것을 나눠줬을 것 같니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}가 개미라면 겨울에 베짱이에게 먹을 것을 나눠줬을 것 같니?", 
                                   pos_bhv="do_compliment_S", pos=f"그럴 수 있겠구나!",
                                   neg_bhv="do_compliment_S", neg=f"그럴 수 있겠구나!",
                                   act_bhv="do_compliment_S", act=f"그럴 수 있겠구나!")

        # 3. 마무리 대화
        pibo = cm.tts(bhv="do_suggestion_S", string=f"열심히 일한 개미에게 칭찬을 해볼까?")
        answer = cm.responses_proc(re_bhv="do_suggestion_S", re_q=f"열심히 일한 개미에게 칭찬을 해볼까?", 
                                   pos_bhv="do_compliment_S", pos=f"정말 잘 하는 걸.?", 
                                   neu_bhv="do_compliment_S", neu=f"괜찮아. 모를 수 있지.", 
                                   act_bhv="do_compliment_S", act=f"정말 잘 하는 걸.?")
        
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
    fat.Ants()
