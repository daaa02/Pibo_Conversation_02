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

sys.path.append('/home/pi/Pibo_Package_04/Pibo_Play/')
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
                
        
    def mus_13(self):
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"신문지 야구 놀이를 해보자!")
        
        time.sleep(1)
        pibo = cm.tts(bhv="do_explain_A", string=f"이번 놀이는 신문지, 종이, 테이프, 그림도구와 가위가 필요해! 준비가 되면 준비 됐다고 말해줘~")
        cwc.writerow(['pibo', pibo])
        
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 준비 됐다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"좋았어. 놀이 방법을 알려줄께!")
                time.sleep(1)                
                pibo = cm.tts(bhv="do_explain_B", string=f"신문지를 뭉쳐서 공을 만들고 야구를 하듯이 방망이로 쳐 볼 거야. ")
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
                pibo = cm.tts(bhv="do_explain_A", string=f"좋았어! 또 종이로 과녁을 만들어서 공으로 맞춰 볼 거야. 준비가 됐으면 시작하자고 말해줘.")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 됐으면 시작하자고 말해줘.")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"그래 시작하자!")
                pibo = cm.tts(bhv="do_explain_A", string=f"먼저 과일 과녁을 만들어 보자. 종이에 좋아하는 과일을 그려서 동그랗게 자르면 돼. 다 했으면 다 했어라고 말해줘.")
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
                pibo = cm.tts(bhv="do_compliment_S", string=f"우와, 정말 멋진 과일 과녁이다.")
                pibo = cm.tts(bhv="do_suggestion_L", string=f"다음은 신문지를 뭉쳐서 공을 만들자. 남은 신문지는 길게 말아서 방망이를 만들어 보는거야. 다 했으면 다 했어 라고 말해줘.")
                break
            else:
                continue      
            
        while True:
            audio.audio_play(filename="/home/pi/Pibo_Package_04/Pibo_Play/data/behavior/audio/sound_body.mp3", volume=-1600)   
            answer = cm.responses_proc(re_bhv="do_waiting_B", re_q=f"다 했으면 다 했어 라고 말해줘.")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                audio.stop
                pibo = cm.tts(bhv="do_compliment_S", string=f"잘했어! 이젠 공을 방망이로 쳐보자")
                pibo = cm.tts(bhv="do_suggestion_L", string=f"{wm.word(self.user_name, 0)}가 먼저 방망이를 잡아. 친구가 공을 던져주면 힘껏 쳐 보는거야. 준비가 됐으면 준비 됐어 라고 말해줘.")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:            
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"준비가 됐으면 준비 됐어 라고 말해줘.")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                time.sleep(1)
                pibo = cm.tts(bhv="do_compliment_S", string=f"좋아, 내가 시작 하면 공을 던지는 거야. ")
                pibo = cm.tts(bhv="do_stop", string=f"준비~이")
                pibo = cm.tts(bhv="do_stop", string=f"시이~작~~!")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
        
        while True:      
            time.sleep(5)
            pibo = cm.tts(bhv="do_compliment_S", string=f"공을 쳤어? 처음엔 원래 잘 안 되는데 그래도 괜찮아. 열심히 하는 모습이 멋져. ")
    
            pibo = cm.tts(bhv="do_suggestion_S", string=f"이번엔 아까 만든 과녁을 테이프로 벽에 붙이고 공을 던져 맞춰보자. 준비가 되면 준비 됐다고 말해줘.")
            time.sleep(5)
            break
            
        while True:            
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"준비가 됐으면 준비 됐어 라고 말해줘.")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"좋아, 어떤 과일을 맞출지 마음 속으로 정하고 공으로 과일을 맞추는 거야. ")
                pibo = cm.tts(bhv="do_waiting_A", string=f"과녁을 맞췄으면 과일 이름을 크게 외쳐줘. ")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue    
        
        while True:            
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"과녁을 맞췄으면 과일 이름을 크게 외쳐줘. ")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            pibo = cm.tts(bhv="do_compliment_S", string=f"와아~ 멋지다아! 집중해서 공을 던지는 모습이 진짜 야구 선수 같았어. ")
            
            time.sleep(1)
            pibo = cm.tts(bhv="do_question_S", string=f"이제 자리에 앉아서 잠시 쉬자. 방망이로 공을 맞추느라 팔에 힘을 많이 주었으니 양 손으로 꾹꾹 눌러볼거야. 10초 동안 마사지 시이작!")
            time.sleep(10)
            pibo = cm.tts(bhv="do_question_S", string=f"팔이 시원해졌지?")
            
            break

        while True: 
            answer = cm.responses_proc(re_bhv="do_waiting_B", re_q=f"또 하고 싶으면 또 하자고 말해줘.")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "no" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"정말 열심히 신문지 야구를 했어. {wm.word(self.user_name, 0)}가 자랑스러워!")
                time.sleep(1)
                pibo = cm.tts(bhv="do_question_S", string=f"신문지 야구놀이 해보니까 어때? 오늘 놀이에서 어려운 게 있었어?")  
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"오늘 놀이에서 어려운 게 있었어?") 
                
                pibo = cm.tts(bhv="do_question_S", string=f"그렇구나. 파이보는 친구랑 놀다가 실수로 친구를 다치게 한 적이 있어. {wm.word(self.user_name, 0)}도 그런 적 있었어?")  
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"파이보는 친구랑 놀다가 실수로 친구를 다치게 한 적이 있어. {wm.word(self.user_name, 0)}도 그런 적 있었어?") 
                
                pibo = cm.tts(bhv="do_joy_B", string=f"그런 일이 있었구나. {wm.word(self.user_name, 0)}는 친구가 다치지 않도록 조심하는 멋진 친구 같아. ")  
                break
            else:
                continue

            
        pibo = cm.tts(bhv="do_stop", string=f"{wm.word(self.user_name, 0)}가 열심히 놀이를 했으니, 오늘은 튼튼 스탬프를 찍어줄께.")
        behavior.do_stamp()
        time.sleep(1)
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"사진을 찍어 줄게! 공과 방망이를 들고 브이를 해봐!")
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
    mus.mus_13()
