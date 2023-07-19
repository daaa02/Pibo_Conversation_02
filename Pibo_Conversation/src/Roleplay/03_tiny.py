# -*- coding: utf-8 -*-

# 역할놀이-작은 존재

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


class Roleplay():    
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = config['user_name'] 
        self.score = []
        self.turns = []
        self.reject = []
        
    
    def Tiny(self):
        
        # 1. 역할 알림
        pibo = cm.tts(bhv="do_suggestion_S", string="역할 놀이를 해볼까?")
        pibo = cm.tts(bhv="do_suggestion_S", string="오늘은 아주 작은 역할을 해보자.") 
        
        # 2. 역할 놀이 (1 of 3)        
        
        animal = (['고양이', '새끼고양이', '고양이는 수영도 잘하고 높은 곳에서도 안전하게 뛰어내릴 수 있다고 해.대단하지 않니?'])

        #role = random.choice([animal[0], animal[1], animal[2]])
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"이제 우리는 {wm.word(animal[1], 0)}야!")
        
        pibo = cm.tts(bhv="do_suggestion_L", string=f"{wm.word(self.user_name, 0)}도 {animal[0]} 소리를 흉내내 보자! 시작!")
        answer = cm.responses_proc(re_bhv="do_suggestion_L", re_q=f"{wm.word(self.user_name, 0)}도 {animal[1]} 울음 소리를 흉내내보자! 시작!",
                                   neu_bhv="do_explain_A", neu=f"{wm.word(animal[0], 2)} 이렇게 울어.",
                                   act_bhv="do_joy_A", act=f"{wm.word(animal[1], 1)} 나타났다!")
        
        audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/16_cat.wav")
        
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
        
        pibo = cm.tts(bhv="do_explain_A", string=f"{animal[2]}. 대단하지 않니?")
        
        
        # 3. 대화 시작        
        # 3.1
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(animal[1], 2)} 작고 약해서 언제 가장 힘들까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(animal[1], 2)} 작고 약해서 언제 가장 힘들까?",
                                   pos_bhv="do_question_S", pos=f"{wm.word(self.user_name, 0)}도 작아서 속상했던 적이 있니?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 대답하기 어려울 수 있어.",
                                   act_bhv="do_question_S", act=f"{wm.word(self.user_name, 0)}도 작아서 속상했던 적이 있니?")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
        
        if answer[0][0] == "action" or answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}도 작아서 속상했던 적이 있니?",
                                       pos_bhv="do_question_S", pos="자세히 이야기해 줄래?",
                                       neu_bhv="do_compliment_S", neu="괜찮아. 대답하기 어려울 수 있어.")

            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
        if answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="자세히 이야기해 줄 수 있니?",
                                        pos_bhv="do_sad", pos=f"{wm.word(self.user_name, 0)}가 속상했겠다.",
                                        neu_bhv="do_compliment_S", neu="괜찮아.말하기 어려울 수 있어.",
                                        act_bhv="do_sad", act=f"{wm.word(self.user_name, 0)}가 속상했겠다.")  
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
        
        # 3.2
        pibo = cm.tts(bhv="do_question_L", string=f"그럼 {wm.word(animal[1], 1)}가 된다면 어떤 점이 가장 좋을까?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(animal[1], 2)} 작고 약해서 언제 가장 힘들까?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 생각나지 않을 수 있어.")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
        
        # 3.3
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 {wm.word(animal[0], 1)} 되어서 몰래 가보고 싶은 곳이 있니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}가 {wm.word(animal[0], 1)} 된다면 어디에 살고 싶니?",
                                   pos_bhv="do_question_S", pos="그 곳에 가서 무엇을 하고 싶니?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 바로 떠오르지 않을 수 있어.")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
        
        if answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="그 곳에 가서 무엇을 하고 싶니?",
                                       neu_bhv="do_compliment_S", neu="괜찮아. 바로 떠오르지 않을 수 있어.",
                                       act_bhv="do_joy_B", act="파이보도 함께 가고 싶다.")      
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
                
        # 4. 마무리 대화
        pibo = cm.tts(bhv="do_joy_A", string=f"{wm.word(animal[0], 2)} 작지만 멋진 친구들이야! 다음에 또 재미있는 역할놀이 하자.")



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
    
    rop = Roleplay()
    rop.Tiny()