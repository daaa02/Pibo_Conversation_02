# -*- coding: utf-8 -*-

# 동화-새끼염소와 늑대

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
            self.user_name = config['user_name'] 
                
        
    def Goat(self):
        
        # 1. 동화 줄거리 대화
        pibo = cm.tts(bhv="do_joy_A", string=f"정말 재미있는 이야기였어! {wm.word(self.user_name, 0)}는 어떤 장면이 재미있었니?")
        answer = cm.responses_proc(re_bhv="do_joy_A", re_q=f"{wm.word(self.user_name, 0)}는 어떤 장면이 재미있었니?",
                                   neu_bhv="do_compliment_S", neu=f"그럴 수 있지.")
        
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 어떤 동물을 좋아하니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 어떤 동물을 좋아하니?", 
                                   pos_bhv="do_question_L", pos=f"그 동물은 어떻게 생겼는지 말해줄래?", 
                                   neu_bhv="do_compliment_S", neu=f"몰라도 괜찮아.", 
                                   act_bhv="do_question_L", act=f"그 동물은 어떻게 생겼는지 말해줄래?")

        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"그 동물은 어떻게 생겼는지 말해줄래?", 
                                       neu_bhv="do_compliment_S", neu=f" 몰라도 괜찮아.")

        pibo = cm.tts(bhv="do_question_S", string=f"염소랑 늑대가 달리기를 하면 누가 더 빠를 것 같니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"염소랑 늑대가 달리기를 하면 누가 더 빠를 것 같니?")

        pibo = cm.tts(bhv="do_question_S", string=f"사냥개 몇 마리가 늑대를 쫓아갔을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"사냥개 몇 마리가 늑대를 쫓아갔을까?", 
                                   act_bhv="do_compliment_S", act=f"그렇게 생각하는구나!")
        
        # 2. 등장인물 공감 대화
        pibo = cm.tts(bhv="do_question_S", string=f"새끼염소가 늑대한테 쫓겼을 때 무서웠을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"새끼염소가 늑대한테 쫓겼을 때 무서웠을까?", 
                                   pos_bhv="do_question_L", pos=f"{wm.word(self.user_name, 0)}가 최근에 무섭다고 느낀 적이 있다면 말해줄래?", 
                                   act_bhv="do_question_L", act=f"{wm.word(self.user_name, 0)}가 최근에 무섭다고 느낀 적이 있다면 말해줄래?")

        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}가 최근에 무섭다고 느낀 적이 있다면 말해줄래?",
                                       pos_bhv="do_compliment_S", pos=f"그랬구나! 정말 무서웠겠다!", 
                                       act_bhv="do_compliment_S", act=f"그랬구나! 정말 무서웠겠다!")

        pibo = cm.tts(bhv="do_question_L", string=f"사냥개들이 새끼 염소를 구해줬을 때 새끼 염소 기분이 기뻤을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"사냥개들이 새끼 염소를 구해줬을 때 새끼 염소 기분이 기뻤을까?", 
                                   pos_bhv="do_question_L", pos=f"{wm.word(self.user_name, 0)}가 도움을 받고 기뻤던 적이 있다면 이야기해 줄래?", 
                                   neu_bhv="do_compliment_S", neu=f" 몰라도 괜찮아.", 
                                   act_bhv="do_question_L", act=f"{wm.word(self.user_name, 0)}가 도움을 받고 기뻤던 적이 있다면 이야기해 줄래?")

        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}가 도움을 받고 기뻤던 적이 있다면 이야기해 줄래?", 
                                       pos_bhv="do_compliment_S", pos=f"그런 일이 있었구나! 정말 기뻤겠다!", 
                                       act_bhv="do_compliment_S", act=f"그런 일이 있었구나! 정말 기뻤겠다!")


        # 3. 마무리 대화
        pibo = cm.tts(bhv="do_question_L", string=f"만약 {wm.word(self.user_name, 0)}가 늑대를 무서워하는 새끼 염소를 만난다면 뭐라고 해줄 수 있을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}가 다양한 모험을 하고 집으로 돌아온 엄지 둥이 에게 위로를 해줘볼까?",  
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
    fat.Goat()