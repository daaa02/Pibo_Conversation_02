# 역할놀이-마법을 부리는 존재

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


class Cog():   
    
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

    
    def cog_3(self):
        pibo = cm.tts(bhv="do_suggestion_S", string=f"종이컵 놀이를 해보자!")
        time.sleep(1)
        pibo = cm.tts(bhv="do_explain_A", string=f"이번 놀이는 종이컵이 필요해! 종이컵 갯수는 많으면 많을수록 좋아. 준비가 되면 준비 됐다고 말해줘~")
        
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비가 되면 준비 됐다고 말해줘~")
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_joy_A", string=f"좋았어. 놀이 방법을 알려줄께!")
                time.sleep(1)                
                pibo = cm.tts(bhv="do_explain_B", string=f"이번 놀이는 종이컵을 던져보고 높게 쌓아보는 놀이야.")
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
                pibo = cm.tts(bhv="do_explain_A", string=f"좋았어! 놀이 전에 먼저 종이컵의 생김새는 어떤지 살펴보자.") 
                time.sleep(1)
                pibo = cm.tts(bhv="do_explain_A", string=f"어떻게 해야 정확하게 던지고 쌓을 수 있을지 생각해봐. 준비가 됐으면 시작하자고 말해줘.")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비 됐으면 준비 됐다고 말해줘!")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_explain_A", string=f"먼저 종이컵을 던져 골인 시킬 곳을 정해봐. 그 곳에 상자나 훌라후프 같은 걸 놓아도 좋아.")
                time.sleep(5)
                pibo = cm.tts(bhv="do_suggestion_S", string=f"이제 종이컵 여러 개를 손에 들고 다섯 발자국 정도 떨어져 서 보자. 준비 됐으면 준비 됐어 라고 말해줘!")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"준비 됐으면 준비 됐어 라고 말해줘!")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_explain_A", string=f"좋아. 이제 종이컵을 골인 시키는거야. 한번에 못 넣으면 또 던져도 돼. 다 넣었으면 다 넣었다고 말해줘!")
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
        while True:
            time.sleep(10)
            answer = cm.responses_proc(re_bhv="do_explain_A", re_q=f"다 넣었으면 다 넣었다고 말해줘!")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_compliment_L", string=f"와, 원래 처음에는 어려운데 잘하는걸?")
                time.sleep(1)
                
                pibo = cm.tts(bhv="do_question_L", string=f"이번에는 종이컵 탑을 쌓아보자. 어떤 모양의 탑을 쌓을지 생각해봐. {wm.word(self.user_name, 0)}는 어떤 모양으로 쌓고 싶어?")
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"어떤 모양으로 쌓고 싶어?")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                
                pibo = cm.tts(bhv="do_compliment_L", string=f"좋은 생각이야! 어떤 모양이든 {wm.word(self.user_name, 0)}만의 탑을 쌓아봐. 끝났으면 끝났어 라고 말해줘!") 
                cwc.writerow(['pibo', pibo])
                break
            else:
                continue
            
            
        while True:
            time.sleep(10)            
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"끝났으면 끝났다고 말해줘~")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_question_L", string=f"잘했어~ 정말 멋지다!")
                
                time.sleep(1)
                pibo = cm.tts(bhv="do_question_L", string=f"이제 자리에 누워 몸 위에 종이컵을 올려놓자. 많이 올릴 수록 좋아~") 
                time.sleep(5)
                pibo = cm.tts(bhv="do_waiting_B", string=f"다 올렸으면 다 올렸다고 말해줘!")
                break
            else:
                continue
        
        while True:
            time.sleep(10)            
            answer = cm.responses_proc(re_bhv="do_waiting_A", re_q=f"다 올렸으면 다 올렸다고 말해줘!")
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
                        
            if answer[0][0] == "done" or answer[0][0] == "yes" or answer[0][0] == "next":
                pibo = cm.tts(bhv="do_explain_A", string=f"좋았어. 이제 내가 하나, 둘, 셋을 세면 벌떡 일어나서 종이컵을 떨어뜨리는 거야.")
                time.sleep(1)
                pibo = cm.tts(bhv="do_joy_A", string=f"자, 준비이~ 하나, 두울, 세엣!")
                audio.audio_play(filename="/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/audio/sound_cup.wav", volume=-1500)
                
                time.sleep(5)
                pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 오늘 종이컵 놀이 하면서 어려운 게 있었어? ")
                answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"오늘 종이컵 놀이 하면서 어려운 게 있었어? ")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                
                pibo = cm.tts(bhv="do_question_L", string=f"그렇구나. 어떻게 하면 파이보도 종이컵 놀이를 잘 할 수 있을까?")
                answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"어떻게 하면 파이보도 종이컵 놀이를 잘 할 수 있을까?")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                
                pibo = cm.tts(bhv="do_question_S", string=f"그렇구나. {wm.word(self.user_name, 0)}의 생각을 들어보니 정말 그런 것 같아! ")                
                break
            else:
                continue
            
        pibo = cm.tts(bhv="do_stop", string=f"{wm.word(self.user_name, 0)}가 열심히 놀이를 했으니, 오늘은 똑똑 스탬프를 찍어줄께.")
        behavior.do_stamp()
        time.sleep(1)
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"사진을 찍어 줄게! 종이컵을 들고 포즈를 취해봐!")        
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
            self.score = [0.0, 0.0, -0.5, 0.0]
        
        if self.aa == "positive":
            cm.tts(bhv="do_joy_A", string=f"나도야! 다음에 또 재미있는 놀이 알려줄게.")
            self.score = [0.0, 0.0, 0.5, 0.0]
            
        if self.aa != "negative" and self.aa != "positive": # if answer[0][0] == "neutral":
            cm.tts(bhv="do_joy_A", string=f"{wm.word(self.user_name, 0)}랑 노는 건 정말 재미있어.")
            self.score = [0.0, 0.0, -0.25, 0.0]
        
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
    
    cog = Cog()
    cog.cog_3()