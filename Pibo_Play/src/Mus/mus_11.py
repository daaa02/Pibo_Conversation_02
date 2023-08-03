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


class Mus():
    
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
                
        
    def mus_11(self):
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"곡식 주머니 옮기기 놀이를 해보자!")
        
        time.sleep(1)
        pibo = cm.tts(bhv="do_explain_A", string=f"이번 놀이는 양말과 양말에 넣을 곡식이 필요해! 곡식은 쌀이나 콩이면 좋아! 준비가 되면 준비 됐다고 말해줘~")
        cwc.writerow(['pibo', pibo])
        
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 준비 됐다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"좋았어. 놀이 방법을 알려줄께!")
                time.sleep(1)                
                pibo = cm.tts(bhv="do_explain_B", string=f"곡식을 넣은 양말은 개미가 열심히 일 해서 마련한 식량이야. 곡식 주머니를 조심히 떨어트리지 않고 머리나 어깨에 얹고 운반해보자!")
                cwc.writerow(['pibo', pibo])
                pibo = cm.tts(bhv="do_question_S", string=f"어렵지 않지? 준비 됐으면 시작하자고 말해줘~")
                break
            
            if answer[0][0] == "no" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_suggestion_S", string=f"그럼 다른 놀이 하자! {wm.word(self.user_name, 0)}가 다시 내 머리를 쓰다듬어주면 돼!")
                self.score = [0.0, 0.0, 0.0, -0.25]
                cwp.writerow([today, filename, self.score[0], self.score[1], self.score[2],self.score[3]])                   
                sys.exit(0)
                
            else:
                continue
        
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비 됐으면 시작하자고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_explain_A", string=f"좋았어! 먼저 곡식주머니를 만들어보자.")
                time.sleep(1)
                pibo = cm.tts(bhv="do_explain_B", string=f"양말에 곡식을 넣은 다음 발목에 묶어줘. 다 했으면 다 했다고 말해줘.")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"다 했으면 다 했다고 말해줘.")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_suggestion_S", string=f"잘했어! 이젠 곡식주머니를 머리에 얹고 가고 싶은 곳까지 움직여보자~ 다 갔으면 다 갔다고 말해줘.")
                cwc.writerow(['pibo', pibo])                
                break
            else:
                continue
            
        while True:
            time.sleep(10)  
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"가고 싶은 곳까지 다 갔으면 다 갔다고 말해줘.")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"잘했어! 이젠 곡식주머니를 호박이라고 생각하고 재료를 들고 가고 싶은 곳까지 움직여보자~ 다 했으면 다 했어 라고 말해줘.")
                break
            else:
                continue      
            
        while True:      
            time.sleep(10)  
            audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_body.mp3", volume=-1600)   
            answer = cm.responses_proc(re_bhv="do_waiting_B", re_q=f"다 했으면 다 했어 라고 말해줘.")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                audio.stop
                time.sleep(1)
                pibo = cm.tts(bhv="do_compliment_S", string=f"우와 정말 잘 하는걸? 다시 돌아가자. ")
                time.sleep(3)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"이제 어깨 위에 두 개를 올리고 이동해봐. 다 왔으면 다 왔다고 말해줘.")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:            
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"목표점까지 다 왔으면 다 왔다고 말해줘.")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                time.sleep(1)
                pibo = cm.tts(bhv="do_compliment_S", string=f"좋았어! 이제 내가 몸 부위를 말하면 곡식주머니를 거기로 옮기고 균형을 잡아봐.")
                time.sleep(1)
                pibo = cm.tts(bhv="do_compliment_S", string=f"내가 배 하면 배에 얹고, 머리 하면 머리에 얹고 떨어뜨리지 않는 거야. 준비됐으면 준비 됐어 라고 말해줘.")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
        
        while True:            
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"준비됐으면 준비 됐어 라고 말해줘.")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_question_S", string=f"좋아~ 시작한다~! 처음은 배!")
                time.sleep(5)
                pibo = cm.tts(bhv="do_question_S", string=f"다음은~ 머리!")
                time.sleep(5)
                pibo = cm.tts(bhv="do_question_S", string=f"다음은~ 손등!")
                time.sleep(5)
                pibo = cm.tts(bhv="do_question_S", string=f"다음은~ 팔!")
                time.sleep(5)
                pibo = cm.tts(bhv="do_question_S", string=f"마지막은 무릎 사이~!")
                time.sleep(5)
                pibo = cm.tts(bhv="do_question_L", string=f"어때? 몇 번이나 떨어뜨렸어?")
                break
            else:
                continue
            
        while True:            
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"몇 번이나 떨어뜨렸어?")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            pibo = cm.tts(bhv="do_compliment_S", string=f"와아~ 정말 대단하다! 개미의 식량을 잘 지켜냈어. 정말 멋져~")
            
            time.sleep(1)
            pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 오늘 곡식주머니를 옮기면서 어디에 올리는 게 가장 재미있었어?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"어디에 올리는 게 가장 재미있었어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_compliment_S", string=f"그렇구나. 어려운 곳도 있었어?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"어려운 곳도 있었어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_compliment_S", string=f"그래도 멋지게 해냈어! {wm.word(self.user_name, 0)}가 즐겁게 참여하는 모습이 보기 좋았어~")
            break          
            
        pibo = cm.tts(bhv="do_stop", string=f"{wm.word(self.user_name, 0)}가 열심히 놀이를 했으니, 오늘은 튼튼 스탬프를 찍어줄께.")
        behavior.do_stamp()
        time.sleep(1)
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"사진을 찍어 줄게! 곡식 주머니를 들고 브이 해봐!")
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
            self.score = [0.0, 0.0, 0.0, -0.5]
        
        if self.aa == "positive":
            cm.tts(bhv="do_joy_A", string=f"나도야! 다음에 또 재미있는 놀이 알려줄게.")
            self.score = [0.0, 0.0, 0.0, 0.5]
            
        if self.aa != "negative" and self.aa != "positive": # if answer[0][0] == "neutral":
            cm.tts(bhv="do_joy_A", string=f"{wm.word(self.user_name, 0)}랑 노는 건 정말 재미있어.")
            self.score = [0.0, 0.0, 0.0, -0.25]
        
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
        gss.write_sheet(name=self.user_name, today=f'(3)_{today}', activities=filename)


if __name__ == "__main__":
    
    mus = Mus()
    mus.mus_11()
