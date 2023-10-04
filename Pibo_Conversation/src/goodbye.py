# -*- coding: utf-8 -*-

# 헤어짐 시나리오

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

class Say():
    
    def __init__(self):
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = config['user_name'] 
        self.score = []
        self.turns = []
        self.reject = []
        
    
    def Goodbye(self):

        pibo = cm.tts(bhv="do_sad", string=f"{wm.word(self.user_name, 4)}, 나는 내일 집에 가야해. ")

        pibo = cm.tts(bhv="do_question_L", string=f"나는 {wm.word(self.user_name, 0)}랑 같이 놀고, 이야기 나눈 시간들이 정말 즐거웠어! {wm.word(self.user_name, 0)}는 어땠니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 어땠어?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])

        pibo = cm.tts(bhv="do_question_L", string=f"그럼 나랑 어떤 이야기를 했던 게 기억에 남니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"나랑 어떤 이야기를 했던 게 기억에 남니?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])

        pibo = cm.tts(bhv="do_question_L", string=f"다음에 나랑 또 만나면 어떤 걸 하고 싶니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"다음에 나랑 또 만나면 어떤 걸 하고 싶니?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])

        pibo = cm.tts(bhv="do_compliment_S", string=f"이야기 해줘서 고마워!")

        pibo = cm.tts(bhv="do_joy_A", string=f"우리 모두 다음에 만나는 날까지 쑥쑥 자라도록 하자. 안녕!")

        self.score = [0.0, 0.0, 0.0, 0.0]        
        cwp.writerow([today, filename, self.score[0], self.score[1], self.score[2],self.score[3]])  
        
        # 4. Paradise framework 기록
        turns = sum((self.reject[i] + 1) * 2 for i in range(len(self.reject)))
        print(turns)
        reject = sum(self.reject) 
        
        cwc.writerow(['Turns', turns])
        cwc.writerow(['Rejections', reject])
        cwc.writerow(['Misrecognitions', ])

        cwc.writerow(['%Turns', ])
        cwc.writerow(['%Rejections', ])
        cwc.writerow(['%Misrecognitions', ])

        # 5. 활동 완료 기록
        gss.write_sheet(name=self.user_name, today=f'(4)_{today}', activities=filename)

if __name__ == "__main__":
    
    say = Say()
    say.Goodbye()   
