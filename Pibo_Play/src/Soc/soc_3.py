# -*- coding: utf-8 -*-

# 사회기술-큰 소리로 이야기 하거나 통화하지 않아요

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


class Soc():
    
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
                
        
    def soc_3(self):
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"신문지 위에 서기 놀이를 해보자!")
        
        time.sleep(1)
        pibo = cm.tts(bhv="do_explain_A", string=f"이번 놀이는 신문지가 필요해!") 
        time.sleep(1)
        pibo = cm.tts(bhv="do_waiting_A", string=f"신문지가 없으면 커다란 종이나 담요도 좋아. 준비가 되면 준비 됐어 라고 말해줘~")
        cwc.writerow(['pibo', pibo])        
        
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 준비 됐다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"좋았어. 놀이 방법을 알려줄께!")
                time.sleep(1)
                pibo = cm.tts(bhv="do_explain_B", string=f"노래가 시작되면 신문지 땅 위에 올라가서 춤을 춰야돼. 노래가 나올 때는 신문지 땅 밖으로 나올 수 없고, 노래가 끝나면 나올 수 있어.")
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
                pibo = cm.tts(bhv="do_explain_A", string=f"노래가 끝나고 다시 시작될 때마다 신문지를 반으로 접어서 땅이 좁아지게 만들 거야. 점점 어렵겠지? 준비가 되면 시작하자고 말해줘~")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 시작하자고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_B", string=f"그래애! 시작하자")
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"노래가 시작되면 먼저 바닥에 신문지를 깔고 신문지 위에 올라가서 마음껏 춤춰보자!")            
                cwc.writerow(['pibo', pibo])

            pibo = cm.tts(bhv="do_waiting_A", string=f"준비가 됐으면 시작하자고 말해줘.")
            break
        
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 시작하자고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_B", string=f"그래애! 시작하자")
                time.sleep(1)

                audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_dancing.mp3", volume=-1800)
                pibo = cm.tts(bhv="do_stop", string=f"노래가 끝났어. 신문지 땅 밖으로 나와도 좋아~")
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"신문지를 반으로 접자. 몇 번 접었는지 이따 물어볼테니 잘 기억해 둬야해. 다 접었으면 다 했다고 말해줘!")
                cwc.writerow(['pibo', pibo])                
                break
            else:
                continue
        
        while True:       
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"다 접었으면 다 했어 라고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_compliment_S", string=f"신문지 땅이 좁아졌구나! 다시 시작해보자!")
                # pibo = cm.tts(bhv="do_suggestion_L", string=f"노래가 다시 시작되면 먼저 바닥에 신문지를 깔고 신문지 위에 올라가서 마음껏 춤춰보자!")            
                
                audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_dancing.mp3", volume=-1800)
                pibo = cm.tts(bhv="do_stop", string=f"노래가 끝났어. 신문지 땅 밖으로 나와도 좋아~")
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"또 신문지를 반으로 접자~ 몇 번 접었는지 이따 물어볼테니 잘 기억해 둬야해. 다 접었으면 다 했다고 말해줘!")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue                 
            
        while True:       
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"다 접었으면 다 했어 라고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_compliment_S", string=f"신문지 땅이 좁아졌구나! 다시 시작해보자!")
                # pibo = cm.tts(bhv="do_suggestion_L", string=f"노래가 다시 시작되면 먼저 바닥에 신문지를 깔고 신문지 위에 올라가서 마음껏 춤춰보자!")            
                
                audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_dancing.mp3", volume=-1800)
                pibo = cm.tts(bhv="do_stop", string=f"노래가 끝났어. 신문지 땅 밖으로 나와도 좋아~")
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"또 신문지를 반으로 접자~ 몇 번 접었는지 이따 물어볼테니 잘 기억해 둬야해. 다 접었으면 다 했다고 말해줘!")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue     
            
        while True:       
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"다 접었으면 다 했어 라고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_compliment_S", string=f"신문지 땅이 좁아졌구나! 다시 시작해보자!")
                # pibo = cm.tts(bhv="do_suggestion_L", string=f"노래가 다시 시작되면 먼저 바닥에 신문지를 깔고 신문지 위에 올라가서 마음껏 춤춰보자!")            
                
                audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_dancing.mp3", volume=-1800)
                pibo = cm.tts(bhv="do_stop", string=f"노래가 끝났어. 신문지 땅 밖으로 나와도 좋아~")
                time.sleep(1)
                pibo = cm.tts(bhv="do_suggestion_L", string=f"신문지를 몇번 접었는지 기억나? 숫자로 몇 번인지 말해줘~")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue 
        
        
        while True:       
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"몇 번 접었는지 숫자로 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])

            if '3' in answer[0][1] or '세' in answer[0][1] or '셋' in answer[0][1]:
                pibo = cm.tts(bhv="do_compliment_S", string=f"대단한걸? {wm.word(self.user_name, 0)}는 기억력이 좋구나!")
                break            
            else:
                pibo = cm.tts(bhv="do_compliment_S", string=f"정답은 세 번이야~!")
                break
            
        while True:            
            pibo = cm.tts(bhv="do_question_S", string=f"춤 추니까 기분이 어땠어? 신났어?")            
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"춤 추니까 기분이 어땠어?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_compliment_S", string=f"그런 기분이 들었구나. 파이보는 같이 노래 듣고 춤춰서 정말 즐거웠어!")
            time.sleep(1)
            
            pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 어떤 노래를 좋아해?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 어떤 노래를 좋아해?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])                 
            
            pibo = cm.tts(bhv="do_question_S", string=f"정말? 왜?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"왜 그 노래를 좋아해?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_question_S", string=f"그렇구나. 나중에 파이보에게도 꼭 불러줘!")
            break
                 
            
            
        pibo = cm.tts(bhv="do_stop", string=f"{wm.word(self.user_name, 0)}가 열심히 놀이를 했으니, 오늘은 바른 스탬프를 찍어줄께.")
        behavior.do_stamp()
        time.sleep(1)
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"사진을 찍어 줄게! 신문지를 들고 브이해봐!")
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
            self.score = [0.0, -0.5, 0.0, 0.0]
        
        if self.aa == "positive":
            cm.tts(bhv="do_joy_A", string=f"나도야! 다음에 또 재미있는 놀이 알려줄게.")
            self.score = [0.0, 0.5, 0.0, 0.0]
            
        if self.aa != "negative" and self.aa != "positive": # if answer[0][0] == "neutral":
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
        gss.write_sheet(name=self.user_name, today=f'(4)_{today}', activities=filename)



if __name__ == "__main__":
    
    soc = Soc()
    soc.soc_3()