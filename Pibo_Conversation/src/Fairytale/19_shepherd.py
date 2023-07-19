# -*- coding: utf-8 -*-

# 동화-양치기 소년과 늑대

import os, sys
import re
import csv
import random
from datetime import datetime
import time
import json

# sys.path.append('/home/kiro/workspace/Conversation_Scenarios/')
sys.path.append('/home/pi/Pibo_Conversation/')
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


class Fairytale():    
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = config['user_name'] 
        self.story_name = '양치기소년과늑대'
        self.score = []
        self.turns = []
        self.reject = []
                
        
    def Shepherd(self):
        
        # 0. 동화 읽어주기
        pibo = cm.tts(bhv="do_breath1", string=f"내가 재미있는 이야기를 들려 줄게. 동화 제목은 {wm.word(self.story_name, 0)}야.")
        f = open('/home/pi/Pibo_Conversation/src/Fairytale/data/19_shepherd_story.txt', 'r')
        lines = f.readlines()
        # print(lines)
        
        for i in range(0, len(lines), 2):
            try:
                text_to_speech(voice="nara", text=f"{lines[i]}")
                text_to_speech(voice="ndain", text=f"{lines[i+1]}")
            except IndexError as e:
                break
        
        # 1. 동화 줄거리 대화        
        pibo = cm.tts(bhv="do_joy_A", string=f"정말 재미있는 이야기였어! {wm.word(self.user_name, 0)}는 어떤 장면이 재미있었니?")
        answer = cm.responses_proc(re_bhv="do_joy_A", re_q=f"{wm.word(self.user_name, 0)}는 어떤 장면이 재미있었니?",
                                   neu_bhv="do_compliment_S", neu=f"그럴 수 있지.")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1]) 
        
        pibo = cm.tts(bhv="do_question_S", string=f"양치기 소년은 양들을 돌볼 때 힘들겠지?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"양치기 소년은 양들을 돌볼 때 힘들겠지?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1]) 
        
        pibo = cm.tts(bhv="do_question_S", string=f"양치기 소년이 돌보는 양은 몇 마리 일지 상상해볼까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"양치기 소년이 돌보는 양은 몇 마리 일지 상상해볼까?",
                                   neu_bhv="do_compliment_S", neu=f"몰라도 괜찮아.")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1]) 
        
        pibo = cm.tts(bhv="do_question_S", string=f"그 많은 양들은 풀을 얼마나 먹을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"그 많은 양들은 풀을 얼마나 먹을까?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1]) 

        # 2. 등장인물 공감 대화        
        pibo = cm.tts(bhv="question_S", string=f"양치기 소년에게 속은 마을 사람들은 화가 났을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"양치기 소년에게 속은 마을 사람들은 화가 났을까?", 
                                   pos_bhv="do_question_S", pos=f"{wm.word(self.user_name, 0)}도 최근에 속아서 화가 난 적이 있다면 말해 줄 수 있니?",
                                   act_bhv="do_question_S", act=f"{wm.word(self.user_name, 0)}도 최근에 속아서 화가 난 적이 있다면 말해 줄 수 있니?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1]) 

        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}도 최근에 속아서 화가 난 적이 있다면 말해 줄 수 있니?",
                                       neu_bhv="do_compliment_S", neu=f"괜찮아. 생각 나지 않을 수 있어.", 
                                       act_bhv="do_sad", act=f"정말 화가 났었겠구나!")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1]) 
            
        pibo = cm.tts(bhv="question_S", string=f"거짓말을 한 양치기 소년은 후회했을까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"거짓말을 한 양치기 소년은 후회했을까?", 
                                   pos_bhv="do_question_S", pos=f"{wm.word(self.user_name, 0)}도 최근에 후회 한 적이 있다면 말해줄래?", 
                                   neu_bhv="do_compliment_S", neu=f"괜찮아. 생각 나지 않을 수 있어.", 
                                   act_bhv="do_question_S", act=f"{wm.word(self.user_name, 0)}도 최근에 후회 한 적이 있다면 말해줄래?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1]) 

        if answer[0][0] == "positive" or answer[0][0] == "action":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}도 최근에 후회 한 적이 있다면 말해줄래?",
                                       pos_bhv="do_sad", pos=f"속상했겠다.",
                                       act_bhv="do_sad", act=f"속상했겠다.")        
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1]) 
            
        # 3. 마무리 대화    
        pibo = cm.tts(bhv="do_question_L", string=f"자꾸 거짓말을 하는 양치기 소년에게 뭐라고 해주고 싶니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"자꾸 거짓말을 하는 양치기 소년에게 뭐라고 해주고 싶니?",  
                                   pos_bhv="do_compliment_S", pos=f"그렇구나!",
                                   neu_bhv="do_compliment_S", neu=f"괜찮아. 모를 수 있지. ",
                                   neg_bhv="do_compliment_S", neg=f"그렇구나!",
                                   act_bhv="do_compliment_S", act=f"그렇구나!")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1]) 
        
        pibo = cm.tts(bhv="do_joy_B", string=f"오늘 동화 재미있었지? 다음에 또 재미있는 동화를 들려줄게.")
        
        
        
        
        # 3. 피드백 수집
        time.sleep(1)                   
        pibo = cm.tts(bhv="do_question_S", string="파이보랑 얘기한 거 재미있었어? 재밌었는지, 별로였는지 얘기해줄래?")
              
        if answer[0][0] == "negative":
            cm.tts(bhv="do_joy_A", string=f"파이보는 {wm.word(self.user_name, 0)}랑 놀아서 재미있었어!")
            self.score = [0.0, -0.5, 0.0, 0.0]
        
        if answer[0][0] == "positive":
            cm.tts(bhv="do_joy_A", string=f"나도야! 다음에 또 재미있는 놀이 알려줄게.")
            self.score = [0.0, 0.5, 0.0, 0.0]
            
        if answer[0][0] != "negative" and answer[0][0] != "positive": # if answer[0][0] == "neutral":
            cm.tts(bhv="do_joy_A", string=f"{wm.word(self.user_name, 0)}랑 노는 건 정말 재미있어.")
            self.score = [0.0, -0.25, 0.0, 0.0]
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"파이보랑 얘기한 거 재미있었어?") 
        
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
    
    fat = Fairytale()
    fat.Shepherd()
