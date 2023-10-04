# -*- coding: utf-8 -*-

# 동화-라푼젤

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
        
        
    def Rapunzel(self):
        
        # 1. 동화 줄거리 대화
  
  
        pibo = cm.tts(bhv="do_question_L", string=f"{self.story} 동화를 들려줄게.")
        pibo = cm.tts(bhv="do_joy_A", string=f"정말 재미있는 이야기였어! {wm.word(self.user_name, 0)}는 어떤 장면이 재미있었니?")
        answer = cm.responses_proc(re_bhv="do_joy_A", re_q=f"정말 재미있는 이야기였어! {wm.word(self.user_name, 0)}는 어떤 장면이 재미있었니?",
                                   neu_bhv="do_compliment_S", neu=f"그럴 수 있지.")
        
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 아래가 내려다 보이는 높은 곳에 가본 적이 있으면 말해줄래?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}는 아래가 내려다 보이는 높은 곳에 가본 적이 있으면 말해줄래?", 
                                   pos_bhv="do_question_S", pos=f"멋진 걸! 무섭진 않았니?", 
                                   neu_bhv="do_compliment_S", neu=f"몰라도 괜찮아.")
        
        if answer[0][0] == "positive":
            answer = cm.responses_proc(bhv="do_question_S", re_q=f"무섭진 않았니?")
            
        pibo = cm.tts(bhv="do_question_S", string=f"주인공 라푼젤이 갇혀있던 탑은 얼마나 클까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"주인공 라푼젤이 갇혀있던 탑은 얼마나 클까?", 
                                   neu_bhv="do_question_S", neu=f"백화점만큼 엄청 클까?")

        if answer[0][0] == "neutral":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"백화점만큼 엄청 클까?",
                                       neu_bhv="do_compliment_S", neu=f"모를 수 있지.")        
        
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}가 라푼젤 이라면 성에서 어떤 놀이를 했을 것 같니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}가 라푼젤 이라면 성에서 어떤 놀이를 했을 것 같니?")
        
        # 2. 등장인물 공감 대화
        pibo = cm.tts(bhv="do_question_S", string=f"성에 갇혀 있던 라푼젤의 기분은 속상했을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"성에 갇혀 있던 라푼젤의 기분은 속상했을까?", 
                                   pos_bhv="do_question_S", pos=f"{wm.word(self.user_name, 0)}가 최근에 속상하다고 느낀 일이 있다면 말해줄래?",
                                   act_bhv="do_question_S", act=f"{wm.word(self.user_name, 0)}가 최근에 속상하다고 느낀 일이 있다면 말해줄래?")
        
        if answer[0][0] == "postive" or answer[0][0] == "action":
            pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}가 최근에 속상하다고 느낀 일이 있다면 말해줄래?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 최근에 속상하다고 느낀 일이 있다면 말해줄래?", 
                                       act_bhv="do_sad", act=f"그랬구나! 정말 속상했겠는 걸?")
        
        
        pibo = cm.tts(bhv="do_question_S", string=f"마법사에게 머리카락이 잘린 라푼젤의 기분은 어땠을 것 같니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"마법사에게 머리카락이 잘린 라푼젤의 기분은 어땠을 것 같니?",
                                   act_bhv="do_question_S", act=f"{wm.word(self.user_name, 0)}도 비슷한 기분을 느낀적이 있다면 이야기해 줄래?")
        
        if answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}도 비슷한 기분을 느낀적이 있다면 이야기해 줄래?", 
                                       act_bhv="do_compliment_S", act=f"그런 일이 있었구나!")
            
        # 3. 마무리 대화
        pibo = cm.tts(bhv="do_suggestion_L", string=f"성에 갇혀 있던 라푼젤에게  {wm.word(self.user_name, 0)}가 위로를 해줘 볼까?")
        answer = cm.responses_proc(re_bhv="do_suggestion_L", re_q=f"성에 갇혀 있던 라푼젤에게  {wm.word(self.user_name, 0)}가 위로를 해줘 볼까?", 
                                   pos_bhv="do_compliment_S", pos=f"{wm.word(self.user_name, 0)}는 그렇게 말해주고 싶구나!", 
                                   neu_bhv="do_compliment_S", neu=f"괜찮아. 위로를 하기 힘들 수 있어.", 
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
    fat.Rapunzel()