# -*- coding: utf-8 -*-

# 문제해결-화를 참을 수 없어

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
                
        
    def Angry(self):
        
        # 1.1 문제 제시
        pibo = cm.tts(bhv="do_sad", string="요즘 자꾸 화가 나고, 화를 참을 수가 없어.")
        
        # 1.2 경험 질문
        pibo = cm.tts(bhv="do_sad", string=f"{wm.word(self.user_name, 0)}는 어떻게 화를 참니?")
        answer = cm.responses_proc(re_bhv="do_sad", re_q=f"{wm.word(self.user_name, 0)}는 어떻게 화를 참니?")    
    
        pibo = cm.tts(bhv="do_question_L", string="화가 날때 화를 참으면 어떤 점이 좋을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="화가 날때 화를 참으면 어떤 점이 좋을까?",
                                   pos_bhv="do_compliment_S", pos="친구들이랑 덜 싸울 수 있겠지?",
                                   neu_bhv="do_explain_A", neu="괜찮아. 모를 수도 있어. 화를 참으면 친구들이랑 덜 싸울 수 있겠지?",
                                   act_bhv="do_compliment_S", act="친구들이랑 덜 싸울 수 있겠지?")

        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 친구가 화를 내면 어떻게 행동하니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 친구가 화를 내면 어떻게 행동하니?",
                                   pos_bhv="do_sad", pos="친구가 화를 내면 무서울 것 같아.",
                                   neu_bhv="do_explain_B", neu="괜찮아. 생각이 나지 않을 수 있어. 친구가 화를 내면 무서울 것 같아.",
                                   act_bhv="do_sad", act="친구가 화를 내면 무서울 것 같아.")

        pibo = cm.tts(bhv="do_question_S", string="파이보가 계속 화를내면 친구들이 무섭게 생각할까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="파이보가 계속 화를내면 친구들이 무섭게 생각할까?",
                                   pos_bhv="do_compliment_S", pos="친구들도 무서워하겠지?",
                                   neu_bhv="do_explain_C", neu="괜찮아. 상상하기 어려울 수 있어. 아마 친구들도 무서워하겠지?",
                                   act_bhv="do_compliment_S", act="친구들도 무서워하겠지?")
            
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 어떤 놀이를 하면 기분 좋아지니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 어떤 놀이를 하면 기분 좋아지니?")
        
        pibo = cm.tts(bhv="do_question_L", string="화가 날 때 재미있는 놀이를 하면 기분이 좋아질까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="화가 날 때 재미있는 놀이를 하면 기분이 좋아질까?",
                                   pos_bhv="do_compliment_S", pos="기분이 좋아질수도 있겠다.",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 상상하기 어려울 수 있어. 재미있는 놀이를 하면 기분이 좋아질수도 있겠다.",
                                   act_bhv="do_compliment_S", act="기분이 좋아질수도 있겠다.")
        # 2.1 문제 해결
        pibo = cm.tts(bhv="do_joy_A", string="파이보도 이제 화를 잘 참을 수 있도록 노력해야겠다. 알려줘서 정말 고마워!")
                            
        
        
        
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
    sol.Angry()