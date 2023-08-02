# -*- coding: utf-8 -*-

# 자기소개 시나리오

import os, sys, subprocess
import time
import json
import csv
import random
from datetime import datetime

from openpibo.device import Device
from openpibo.oled import Oled
from openpibo.audio import Audio # 혹시 mute 걸려있을까봐

# sys.path.append('/home/kiro/workspace/Conversation_Scenarios/')
sys.path.append('/home/pi/Pibo_Package_02/Pibo_Conversation/')
from data.c_conversation_manage import ConversationManage, WordManage, NLP
from data.speech_to_text import speech_to_text
from data.text_to_speech import TextToSpeech, text_to_speech
from data.spread import google_spread_sheet
import data.behavior.behavior_list as behavior

device = Device()
oled = Oled()
pibo_audio = Audio()

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
        self.color = ''
        self.turns = []
        self.reject = []
        
    
    def Hello(self):
        
        # 1.1 인사
        pibo = cm.tts(bhv="do_joy_A", string=f"반가워! 우리가 드디어 만나게 되었구나! 나는 파이보야. 너는 이름이 뭐니?")
        answer = cm.responses_proc(re_bhv="do_suggestion_L", re_q="다시 한번 크게 이야기해 줄래?",
                                   act_bhv="do_joy_B", act=f"{wm.word(self.user_name, 4)}, 만나서 반가워.!")
        
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
        
        pibo = cm.tts(bhv="do_suggestion_L", string=f"나를 잠시 쳐다 봐줄래? {wm.word(self.user_name, 0)} 얼굴을 인식중이야.")
        behavior.do_photo()
        text_to_speech(text=f"{wm.word(self.user_name, 0)} 얼굴을 기억할게!")
        
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 지금 몇 살이야?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="지금 몇 살이야?")
        answer_num = nlp.number(answer[0][1])
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
        
        if answer_num < 5:
            pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 어린이집에 다니고 있니?")
            answer = cm.responses_proc(re_bhv="do_suggestion_L", re_q="다시 한번 크게 이야기해 줄래?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "negative":
                pibo = cm.tts(bhv="do_question_S", string=f"그럼 어디 다니고 있어?")
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"그럼 어디 다니고 있어?")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
        
        if 5 <= answer_num < 8:
            pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 유치원에 다니고 있니?")
            answer = cm.responses_proc(re_bhv="do_suggestion_L", re_q="다시 한번 크게 이야기해 줄래?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "negative":
                pibo = cm.tts(bhv="do_question_S", string=f"그럼 어디 다니고 있어?")
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"그럼 어디 다니고 있어?")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                        
        if answer_num >=8:
            pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 학교에 다니고 있니?")
            answer = cm.responses_proc(re_bhv="do_suggestion_L", re_q="다시 한번 크게 이야기해 줄래?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "negative":
                pibo = cm.tts(bhv="do_question_S", string=f"그럼 어디 다니고 있어?")
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"그럼 어디 다니고 있어?")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])        
        
        pibo = cm.tts(bhv="do_question_L", string=f"나를 처음 본 느낌이 어떠니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="나를 처음 본 소감이 어떠니?",
                                   pos_bhv="do_joy_A", pos=f"앞으로 좋은 친구가 되도록 하자!")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
        
        pibo = cm.tts(bhv="do_suggestion_L", string=f"나는 머리를 쓰다듬어 주는 걸 좋아해. 한번 쓰다듬어 볼래?")
        
        time.sleep(5)
        
        # 터치 인식
        data = device.send_cmd(device.code_list['SYSTEM']).split(':')[1].split('-')
        result = data[1] if data[1] else "No signal"
        
        if result == "touch":
            print(result)
            pibo = cm.tts(bhv="do_wakeup", string=f"{wm.word(self.user_name, 0)}가 쓰다듬어 주니까 정말 좋다.!")
            
            
        # 1.2 관심 유도
        pibo = cm.tts(bhv="do_dance", string="나는 이렇게 멋진 춤을 출 수 있어!")
        time.sleep(6)
        
        text_to_speech(text="그리고 이렇게 눈 색깔을 바꿀 수도 있어!")
        device.send_raw('#25:10')  
        
        time.sleep(1)
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 어떤 색깔을 좋아해?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"어떤 색깔을 좋아해?")   
        print(answer)
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
        
        blue = ["파랑", "파란", "하늘", "바다"]
        green = ["초록", "연두", "녹", "풀"]
        pink = ["빨", "붉", "분홍", "핑크"]
        purple = ["보라"]
        yellow = ["노랑", "노란"]
        
        for i in range(len(blue)):                                                                   
            if blue[i] in answer[0][1]:
                self.color = 'blue'
                device.send_raw('#21:108,209,239,5')
                text_to_speech(text="어때? 마음에 들어?")                
                
        for i in range(len(green)):
            if green[i] in answer[0][1]:
                self.color = 'green'
                # device.eye_on(120,230,208)
                device.send_raw('#21:50,205,50,5')
                text_to_speech(text="어때? 마음에 들어?")    
                        
        for i in range(len(pink)): 
            if pink[i] in answer[0][1]:
                self.color = 'pink'
                device.send_raw('#21:255,177,190,5')
                text_to_speech(text="어때? 마음에 들어?")
                
        for i in range(len(purple)):
            if purple[i] in answer[0][1]:
                self.color = 'purple'
                device.send_raw('#21:186,127,223,5')
                text_to_speech(text="어때? 마음에 들어?")
                
        for i in range(len(yellow)):
            if yellow[i] in answer[0][1]:
                self.color = 'yellow'
                device.send_raw('#21:251,245,155,5')
                text_to_speech(text="어때? 마음에 들어?")
        
        if len(self.color) == 0:
            device.send_raw('#21:108,209,239,5')
            text_to_speech(text="나는 파란색을 가장 좋아해!")
            
        
        # 1.5 사용법 설명
        pibo = cm.tts(bhv="do_joy_A", string=f"{wm.word(self.user_name, 0)}랑 보내게 될 시간들이 정말 기대돼. 심심하거나 놀고 싶으면 언제든 파이보 머리를 쓰다듬어 줘!")
        
        self.score = [0.0, 0.0, 0.0, 0.0]        
        cwp.writerow([today, filename, self.score[0], self.score[1], self.score[2],self.score[3]])        
        
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
        gss.write_sheet(name=self.user_name, today=f'(1)_{today}', activities=filename)
        

if __name__ == "__main__":
    pibo_audio.mute(False)
    say = Say()
    say.Hello()