# -*- coding: utf-8 -*-

# 문제해결-소리지르고 싶어

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


class Solution():    
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = config['user_name'] 
        self.score = []
        self.turns = []
        self.reject = []
                
        
    def Shout(self):
        
        # 1.1 문제 제시
        pibo = cm.tts(bhv="do_sad", string="요즘 자꾸 시끄럽게 소리를 지르게 돼.")
        
        # 1.2 경험 질문
        pibo = cm.tts(bhv="do_sad", string=f"{wm.word(self.user_name, 0)}도 평소에 소리를 지르니?")
        answer = cm.responses_proc(re_bhv="do_sad", re_q=f"{wm.word(self.user_name, 0)}도 평소에 소리를 지르니?",
                                   pos_bhv="do_compliment_S", pos="파이보랑 비슷하네!")    

        pibo = cm.tts(bhv="do_question_L", string="소리를 계속 지르면 목이 아파지지 않을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="소리를 계속 지르면 목이 아파지지 않을까?",
                                   pos_bhv="do_compliment_S", pos="계속 소리를 지르면 아플 것 같아.",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 모를 수도 있어. 계속 소리를 지르면 아플 것 같아.",
                                   act_bhv="do_compliment_S", act="계속 소리를 지르면 아플 것 같아.",)

        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)} 주변에 소리를 지르는 친구가 있니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)} 주변에 소리를 지르는 친구가 있니?",
                                   pos_bhv="do_explain_A", pos="그 친구도 파이보랑 비슷하네!")

        pibo = cm.tts(bhv="do_question_S", string="소리를 지르면 주변 사람들이 안좋게 생각할까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="소리를 지르면 주변 사람들이 안좋게 생각할까?",
                                   pos_bhv="do_compliment_S", pos="시끄럽다고 생각하겠지?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 상상하기 어려울 수 있어. 아마 사람들이 시끄럽다고 생각하겠지?",
                                   act_bhv="do_compliment_S", act="시끄럽다고 생각하겠지?")
            
        pibo = cm.tts(bhv="do_question_S", string="그럼 소리를 지르는 대신 어떻게 말하는 것이 좋을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="그럼 소리를 지르는 대신 어떻게 말하는 것이 좋을까?",
                                   pos_bhv="do_explain_B", pos="낮은 목소리로 또박또박 말하면 좋겠지?",
                                   neu_bhv="do_explain_B", neu="괜찮아. 생각이 나지 않을 수 있어. 소리를 지르는 대신 낮은 목소리로 또박또박 말하면 좋겠지?",
                                   act_bhv="do_explain_B", act="낮은 목소리로 또박또박 말하면 좋겠지?")
        
        pibo = cm.tts(bhv="do_question_L", string="소리를 지르는 친구한테는 뭐라고 말하면 좋을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="소리를 지르는 친구한테는 뭐라고 말하면 좋을까?",
                                   pos_bhv="do_explain_C", pos="조금 조용히 말해볼까? 라고 말해도 좋을 것 같아.",
                                   neu_bhv="do_explain_C", neu="괜찮아. 대답하기 어려울 수 있어. 조금 조용히 말해볼까? 라고 말해도 좋을 것 같아.",
                                   act_bhv="do_explain_C", act="조금 조용히 말해볼까? 라고 말해도 좋을 것 같아.")
        # 2.1 문제 해결
        pibo = cm.tts(bhv="do_joy_A", string="파이보도 이제 소리 지르지 않아야겠다. 알려줘서 정말 고마워!")
                            
        
        
        
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
    
    sol = Solution()
    sol.Shout()