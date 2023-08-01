# -*- coding: utf-8 -*-

# 문제해결-혼나서 속상해

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


class Solution():    
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = config['user_name'] 
        self.score = []
        self.turns = []
        self.reject = []
                
        
    def Upset1(self):
        
        # 1.1 문제 제시
        pibo = cm.tts(bhv="do_sad", string="한 번 혼나고 나면 오랫동안 기분이 안 좋아.")
        
        # 1.2 경험 질문
        pibo = cm.tts(bhv="do_sad", string=f"{wm.word(self.user_name, 0)}도 한번씩 혼이 나니?")
        answer = cm.responses_proc(re_bhv="do_sad", re_q=f"{wm.word(self.user_name, 0)}도 한번씩 혼이 나니?",
                                   pos_bhv="do_sad", pos=f"{wm.word(self.user_name, 0)}도 속상했겠다.")    
    
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 혼나면 어떻게 하니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}는 혼나면 어떻게 하니?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 말하기 어려울 수 있어.")

        pibo = cm.tts(bhv="do_question_L", string=f"주변에서 누가 가장 {wm.word(self.user_name, 0)}를 많이 혼내니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"주변에서 누가 가장 {wm.word(self.user_name, 0)}를 많이 혼내니?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 말하기 어려울 수 있어.")

        pibo = cm.tts(bhv="do_question_S", string="혼내는 사람의 마음도 속상할까? ")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="혼내는 사람의 마음도 속상할까? ",
                                   pos_bhv="do_compliment_S", pos="혼내는 사람도 속상할 것 같아.",
                                   neu_bhv="do_compliment_S", neu="몰라도 괜찮아.",
                                   act_bhv="do_compliment_S", act="혼내는 사람도 속상할 것 같아.")
        
        pibo = cm.tts(bhv="do_question_L", string="혼나고 나서 어떻게 하면 기분이 좋아질까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="화가 날 때 재미있는 놀이를 하면 기분이 좋아질까?",
                                   pos_bhv="do_compliment_S", pos="기분이 좋아지겠다.",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어.")
        
        pibo = cm.tts(bhv="do_question_L", string="혼난 친구에게 무슨 말을 해주면 좋을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="혼난 친구에게 무슨 말을 해주면 좋을까?",
                                   pos_bhv="do_compliment_S", pos="친구에게 도움이 되겠는 걸?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어.",
                                   act_bhv="do_compliment_S", act="친구에게 도움이 되겠는 걸?")
        
        # 2.1 문제 해결
        pibo = cm.tts(bhv="do_joy_A", string="파이보도 혼나고 나서 기분이 좋아지도록 노력해야겠다. 알려줘서 정말 고마워!")
                            
        
        
        
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
    sol.Upset1()