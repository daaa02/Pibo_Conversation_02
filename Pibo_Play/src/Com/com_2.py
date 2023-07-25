# -*- coding: utf-8 -*-

# 사회기술-차례대로 순서를 지켜요

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
        self.animal = ''
        self.aa = ''
        self.score = []
        self.turns = []
        self.reject = []
        
        self.Positive = ['pos', '좋아', '좋은', '좋았', '좋다', '재미있', '재미 있', '재밌', '재밌어']
        self.Negative = ['neg', '별로', '아니', '안 해', '안해', '안 할래', '안 하', '싫어', '싫', '재미없', '재미 없']
        self.Neutral = ['neu', '글쎄', '몰라', '모르', '몰라', '몰랐', '보통']  
                
        
    def com_2(self):
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"마술에 걸린 동물들 놀이를 해보자!")
        
        time.sleep(1)
        pibo = cm.tts(bhv="do_explain_A", string=f"이번 놀이는 마법지팡이로 쓸 막대기가 필요해! 준비가 되면 준비 됐다고 말해줘~")
        cwc.writerow(['pibo', pibo])
        
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 준비 됐다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"좋았어. 놀이 방법을 알려줄께!")
                time.sleep(1)
                pibo = cm.tts(bhv="do_explain_B", string=f"파이보가 마법사 역할을 할게. {wm.word(self.user_name, 0)}가 동물을 진짜같이 재미있게 표현해줘!")
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
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"할 수 있으면 할 수 있다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_explain_A", string=f"마법사가 그대로 멈춰라!!")
                pibo = cm.tts(bhv="do_stop", string=f"라고 말하면 제자리에서 멈춰야돼! 시작해볼까? 준비가 되면 시작하자고 말해줘~")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 시작하자고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_B", string=f"좋아아! 시작하자")
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"{wm.word(self.user_name, 0)}는 어떤 동물을 좋아해?")  
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue                         
        
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_B", re_q=f"어떤 동물을 좋아해?")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            self.animal = nlp.animal(answer[0][1])
            
            if len(self.animal) != 0:
                pibo = cm.tts(bhv="do_joy_B", string=f"좋았어! {wm.word(self.animal, 0)}로 변해라, 얍!")
                audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_magician.wav", volume=-1500, background=False)
                time.sleep(5) 
                
                pibo = cm.tts(bhv="do_joy_A", string=f"정말 실감나는 걸? 또 주문을 걸게~ 그대로 멈춰라, 얍!")
                audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_magician.wav", volume=-1500, background=False)
                time.sleep(5) 
                
                pibo = cm.tts(bhv="do_joy_B", string=f"이제 마법이 풀렸어! 이번에는 {wm.word(self.user_name, 0)}로 변해라, 얍!")
                audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_magician.wav", volume=-1500, background=False)
                time.sleep(5) 
                
                pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 지금 무엇을 하고 있어?")
                cwc.writerow(['pibo', pibo])
                break
            
            if len(self.animal) == 0 and len(answer[0][1]) != 0:
                self.animal = "그 동물"
                pibo = cm.tts(bhv="do_joy_B", string=f"좋았어! {wm.word(self.user_name, 0)}가 좋아하는 동물로 변해라, 얍!")
                audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_magician.wav", volume=-1500, background=False)
                time.sleep(5) 
                
                pibo = cm.tts(bhv="do_joy_A", string=f"정말 실감나는 걸? 또 주문을 걸게~ 그대로 멈춰라, 얍!")
                audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_magician.wav", volume=-1500, background=False)
                time.sleep(5) 
                
                pibo = cm.tts(bhv="do_joy_B", string=f"이제 마법이 풀렸어! 이번에는 {wm.word(self.user_name, 0)}로 변해라, 얍!")
                audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_magician.wav", volume=-1500, background=False)
                time.sleep(5) 
                
                pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 지금 무엇을 하고 있어?")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"{wm.word(self.user_name, 0)}는 지금 무엇을 하고 있어?")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            pibo = cm.tts(bhv="do_compliment_S", string=f"그렇구나~ {wm.word(self.user_name, 0)}는 표현을 정말 잘 하는 것 같아!")
            time.sleep(1)
            pibo = cm.tts(bhv="do_compliment_L", string=f"{wm.word(self.user_name, 0)}가 오늘 동물 표현을 정말 실감나게 잘했어~ 진짜 동물이 나타난 줄 알고 깜짝 놀랐어!")
            time.sleep(1)
            pibo = cm.tts(bhv="do_suggestion_L", string=f"이제 자리에 앉아 잠시 쉬어보자!")
            time.sleep(3)
            pibo = cm.tts(bhv="do_suggestion_L", string=f"{wm.word(self.user_name, 0)}가 좋아하는 {wm.word(self.animal, 2)} 어떻게 잠을 잘까? 잠자는 모습도 표현해 보자~")
            audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_magician.wav", volume=-1500, background=False)
            pibo = cm.tts(bhv="do_sad", string=f"파이보도 잠이 올 것만 같아. {wm.word(self.user_name, 0)}는 왜 {wm.word(self.animal, 3)} 좋아해?")
            cwc.writerow(['pibo', pibo])
            break
         
        while True:
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 왜 {wm.word(self.animal, 3)} 좋아해?")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            pibo = cm.tts(bhv="do_compliment_S", string=f"그렇구나. 파이보가 기억해 둘게.")
            break            
            
        pibo = cm.tts(bhv="do_stop", string=f"{wm.word(self.user_name, 0)}가 열심히 놀이를 했으니, 오늘은 술술 스탬프를 찍어줄께.")
        behavior.do_stamp()
        time.sleep(1)
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"사진을 찍어 줄게! {self.animal} 처럼 포즈를 취해봐!")
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
        today_end = datetime.now().strftime('%m%d_%H%M')        
        gss.write_sheet(name=self.user_name, today=f'end_{today_end}', activities=filename)

if __name__ == "__main__":
    
    com = Com()
    com.com_2()