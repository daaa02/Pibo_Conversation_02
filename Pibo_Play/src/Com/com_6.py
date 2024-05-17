# -*- coding: utf-8 -*-

# 의사소통-마법사의 보물

import os, sys
import re
import csv
import random
from datetime import datetime
import time
import json

# sys.path.append('/home/kiro/workspace/Conversation_Scenarios/')

sys.path.append('/home/pi/Pibo_Package_02/Pibo_Play/')
from data.p_conversation_manage import ConversationManage, WordManage, NLP
from data.speech_to_text import speech_to_text
from data.text_to_speech import TextToSpeech, text_to_speech
import data.behavior.behavior_list as behavior
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


class Com():
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = config['user_name'] 
        self.aa = ''
        self.score = []
        self.turns = []
        self.reject = []
        
        self.Positive = ['pos', '좋아', '좋은', '좋았', '좋다', '재미있', '재미 있', '재밌', '재밌어']
        self.Negative = ['neg', '별로', '아니', '안 해', '안해', '안 할래', '안 하', '싫어', '싫', '재미없', '재미 없']
        self.Neutral = ['neu', '글쎄', '몰라', '모르', '몰라', '몰랐', '보통']    
                
        
    def com_6(self):
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"마법사의 보물 놀이를 해보자!")
        
        time.sleep(1)
        pibo = cm.tts(bhv="do_explain_B", string=f"이번 놀이는 마법 지팡이가 필요해. 마법 지팡이가 없다면 긴 막대기를 준비해도 좋아 ~") 
        pibo = cm.tts(bhv="do_waiting_B", string=f"준비가 되면 준비 됐다고 말해줘~")
        cwc.writerow(['pibo', pibo])
        
        while True:
            time.sleep(2)
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 준비 됐다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"좋았어. 놀이 방법을 알려줄께!")
                time.sleep(1)
                pibo = cm.tts(bhv="do_explain_B", string=f"먼저 {wm.word(self.user_name, 0)}가 보물을 숨기면 친구가 보물을 찾을거야. OO이는 친구가 보물을 찾기 어렵게 거북이나 나무늘보처럼 느린 동물로 변하는 마법을 거는거야.")
                cwc.writerow(['pibo', pibo])
                pibo = cm.tts(bhv="do_question_S", string=f"할 수 있지? 할 수 있으면 할 수 있다고 말해줘~")
                break
            
            if answer[0][0] == "no":
                pibo = cm.tts(bhv="do_suggestion_S", string=f"그럼 다른 놀이 하자! {wm.word(self.user_name, 0)}가 다시 내 머리를 쓰다듬어주면 돼!")
                self.score = [0.0, 0.0, 0.0, -0.25]
                cwp.writerow([today, filename, self.score[0], self.score[1], self.score[2],self.score[3]])       
                sys.exit(0)
                
            else:
                continue
        
        while True: 
            time.sleep(0.5)
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"할 수 있으면 할 수 있다고 말해줘~")
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_explain_A", string=f"동물 마법은 10초동안 유지되고, 한 번 마법을 건 동물로는 또 마법을 걸 수 없어. ")
                pibo = cm.tts(bhv="do_explain_A", string=f"준비가 되면 시작하자고 말해줘~")
                cwc.writerow(['pibo', pibo])                
                break
            else:
                continue
            
        while True: 
            time.sleep(0.5)        
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 시작하자고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_B", string=f"좋아아! 시작하자")
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"{wm.word(self.user_name, 0)}가 먼저 보물 쪽지를 만들어서 숨겨줘. 다 숨기고 나면 준비 됐어 라고 말해줘~")  
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue                         
        
        while True: 
            time.sleep(7) 
            answer = cm.responses_proc(re_bhv="do_waiting_B", re_q=f"다 숨기고 나면 준비 됐어 라고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_B", string=f"좋아. 마법을 걸 동물카드를 파이보에게 먼저 보여주고 동물 주문을 걸어줘.")
                pibo = cm.tts(bhv="do_explain_A", string=f"카드가 없으면 동물 이름을 말해도 좋아. 동물 이름을 말하고")
                pibo = cm.tts(bhv="do_stop", string=f"변해라 야압! 이라고 하면 돼~")
                time.sleep(1)   
                pibo = cm.tts(bhv="do_joy_A", string=f"시이작~!")
                break
            else:
                continue
    
        #1    
        while True:      
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"동물 이름을 말하고 변해라 야압! 이라고 하면 돼~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_magician.wav", volume=-1500, background=False)
            time.sleep(5)
            pibo = cm.tts(bhv="do_explain_B", string=f"마법이 풀렸어~ 같은 방법으로 다시 마법을 걸어보자. 시이작!")            
            
            audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_magician.wav", volume=-1500, background=False)
            time.sleep(5)
            pibo = cm.tts(bhv="do_explain_B", string=f"마법이 풀렸어~ 보물을 찾으면 찾았다고 말해줘~")    
            break       
        
        
        while True: 
            answer = cm.responses_proc(re_bhv="do_waiting_B", re_q=f"보물을 찾으면 찾았다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_B", string=f"정말 주문을 잘 걸었어~ ")
                pibo = cm.tts(bhv="do_explain_A", string=f"이번에는  역할을 바꿔보자. 친구가 보물을 숨기고 {wm.word(self.user_name, 0)}가 보물을 찾아줘")
                pibo = cm.tts(bhv="do_stop", string=f"보물을 다 숨기고 나면 준비됐어라고 말해줘")
                break
            else:
                continue

        #2
        while True:      
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"동물 이름을 말하고 변해라 야압! 이라고 하면 돼~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_magician.wav", volume=-1500, background=False)
            time.sleep(5)
            pibo = cm.tts(bhv="do_explain_B", string=f"마법이 풀렸어~ 같은 방법으로 다시 마법을 걸어보자. 시이작!")            
            
            audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_magician.wav", volume=-1500, background=False)
            time.sleep(5)
            pibo = cm.tts(bhv="do_explain_B", string=f"마법이 풀렸어~ 보물을 찾으면 찾았다고 말해줘~")    
            break     
        
        while True: 
            answer = cm.responses_proc(re_bhv="do_waiting_B", re_q=f"보물을 찾으면 찾았다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"벌써? 대단한 걸?")
                time.sleep(2)
                pibo = cm.tts(bhv="do_question_S", string=f"한번 더 해볼까? 또 하고 싶으면 또 하자고 말해줘.")
                break
            else:
                continue
            
        
        while True: 
            answer = cm.responses_proc(re_bhv="do_waiting_B", re_q=f"또 하고 싶으면 또 하자고 말해줘.")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "no" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"보물을 열심히 지키고 찾느라 수고했어!")
                break
            else:
                continue
                
            
        while True:          
            pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 보물을 지키는게 재미있었어 아니면 찾는게 재미있었어?")            
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"보물을 지키는게 재미있었어 아니면 찾는게 재미있었어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_compliment_S", string=f"정말? 왜애?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"왜애?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_compliment_S", string=f"그렇구나. 파이보는 {wm.word(self.user_name, 0)}가 다양한 동물을 알아서 정말 신났어!")
            
            pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 어떤 동물을 제일 잘 따라하는 것 같아?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 어떤 동물을 제일 잘 따라하는 것 같아?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_joy_A", string=f"맞아. 파이보도 정말 깜짝 놀랐어!")
            
            break
            
            
        pibo = cm.tts(bhv="do_stop", string=f"{wm.word(self.user_name, 0)}가 열심히 놀이를 했으니, 오늘은 술술 스탬프를 찍어줄께.")
        behavior.do_stamp()
        time.sleep(1)
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"사진을 찍어 줄게! 마법 지팡이를 들고 브이해봐!")        
        behavior.do_photo()
        
        
        # 3. 피드백 수집
        time.sleep(1)                   
        pibo = cm.tts(bhv='do_question_S', string="파이보랑 노는 거 재미있었어? 재밌었는지, 별로였는지 얘기해줄래?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"파이보랑 노는 거 재미있었어?")
        
        if len(answer[0][1]) != 0:
            for i in range(len(self.Negative)):
                if self.Negative[i] in answer[0][1]:
                    self.aa = 'negative'          
            for j in range(len(self.Positive)):
                if self.Positive[j] in answer[0][1]:
                    self.aa = 'positive'                
            if len(self.aa) == 0: 
                self.aa = 'else'

        if self.aa == "negative":
            cm.tts(bhv="do_joy_A", string=f"파이보는 {wm.word(self.user_name, 0)}랑 놀아서 재미있었어!")
            self.score = [-0.5, 0.0, 0.0, 0.0]
        
        if self.aa == "positive":
            cm.tts(bhv="do_joy_A", string=f"나도야! 다음에 또 재미있는 놀이 알려줄게.")
            self.score = [0.5, 0.0, 0.0, 0.0]
            
        if self.aa != "negative" and self.aa != "positive": # if answer[0][0] == "neutral":
            cm.tts(bhv="do_joy_A", string=f"{wm.word(self.user_name, 0)}랑 노는 건 정말 재미있어.")
            self.score = [-0.25, 0.0, 0.0, 0.0]
        
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
        gss.write_sheet(name=self.user_name, today=f'(4)_{today}', activities=filename)
        



if __name__ == "__main__":
    
    com = Com()
    com.com_6()
