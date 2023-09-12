# -*- coding: utf-8 -*-

# 역할놀이-비행하는 존재

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


class Roleplay():    
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = "예진" 
        self.count = 0
        self.score = []
        self.turns = []
        self.reject = []
        
    
    def Flying(self):
        
        # 1. 역할 알림
        pibo = cm.tts(bhv="do_suggestion_S", string="역할 놀이를 해볼까?")
        pibo = cm.tts(bhv="do_suggestion_S", string="오늘은 하늘을 나는 역할을 해보자.") 
                
        # 2. 역할 놀이 (1 of 3)        
        animal = (['새', '하늘에사는큰새', '세상에서 가장 큰 새는 타조라고 해! 타조는 날 수 없는 대신 엄청 빠르게 뛸 수 있어. 멋지지 않니?'],
                  ['나비', '숲속의나비', '나비는 입 뿐만이 아니라 발로도 맛을 느낄 수 있다고 해. 신기하지 않니? '],
                  ['천사', '날개가달린천사', '천사는 심부름꾼이라는 뜻을 가지고 있다고 해. 신기하지 않니?'])
        
        role = random.choice([animal[0], animal[1], animal[2]])
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"이제 우리는 {wm.word(role[1], 0)}야!")
        
        pibo = cm.tts(bhv="do_suggestion_L", string=f"{wm.word(self.user_name, 0)}도 {role[0]} 소리를 흉내내 보자! 시작!")
        answer = cm.responses_proc(re_bhv="do_suggestion_L", re_q=f"{wm.word(self.user_name, 0)}도 {role[0]} 울음 소리를 흉내내보자! 시작!",
                                   neu_bhv="do_explain_A", neu=f"{wm.word(role[0], 2)} 소리를 흉내내볼게!",
                                   act_bhv="do_joy_A", act=f"{wm.word(role[0], 1)} 나타났다!")
        # audio.audio_play(filename)
        pibo = cm.tts(bhv="do_explain_B", string=role[2])
        
        # 3. 대화 시작 (3 of 6 )
        rand = random.sample(range(1,7), 3)
        
        while True:
            for i in range(len(rand)):
                if rand[i] == 1:
                    pibo = cm.tts(bhv="do_explain_A", string="파이보는 마음이 답답할 때 하늘을 날고 싶어.")    
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 언제 {(role[0])}처럼 날고 싶니?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}는 언제 {(role[0])}처럼 날고 싶니?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 생각나지 않을 수 있어.",
                                               act_bhv="do_question_S", act="하늘을 날면 어떤 기분일까?")        
                    
                    if answer[0][0] == "action":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q="하늘을 날면 어떤 기분일까?",
                                                   pos_bhv="do_compliment_S", pos="하늘을 날면 정말 멋지겠다!",
                                                   neu_bhv="do_compliment_S", neu="상상하기 어려울 수도 있어.",
                                                   act_bhv="do_compliment_S", act="하늘을 날면 정말 멋지겠다!")
                    self.count += 1 
                    
                if rand[i] == 2: 
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(role[0], 1)} 되면 어디로 날아가고 싶니?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(role[0], 1)} 되면 어디로 날아가고 싶니?",
                                               pos_bhv="do_question_S", pos="그곳에 가서 무엇을 하고 싶니?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수도 있어.",
                                               act_bhv="do_question_S", act="그곳에 가서 무엇을 하고 싶니?")
                    
                    if answer[0][0] == "positive" or answer[0][0] =="action":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q="그곳에 가서 무엇을 하고 싶니?",
                                                   pos_bhv="do_compliment_S", pos="파이보도 같이 가고 싶은 걸?",
                                                   neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수도 있어.",
                                                   act_bhv="do_compliment_S", act="파이보도 같이 가고 싶은 걸?")
                    self.count += 1
                    
                if rand[i] == 3: 
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(role[0], 1)} 되면 누구와 함께 날아보고 싶니?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(role[0], 1)} 되면 누구와 함께 날아보고 싶니?",
                                               pos_bhv="do_question_S", pos="함께 어디로 가고 싶니?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 바로 떠오르지 않을 수 있어.",
                                               act_bhv="do_question_S", act="함께 어디로 가고 싶니?")
                    
                    if answer[0][0] == "positive" or answer[0][0] =="action":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q="함께 어디로 가고 싶니?",
                                                   pos_bhv="do_compliment_S", pos="파이보도 같이 가고 싶은 걸?",
                                                   neu_bhv="do_compliment_S", neu="괜찮아. 바로 떠오르지 않을 수 있어.",
                                                   act_bhv="do_compliment_S", act="파이보도 같이 가고 싶은 걸?")
                    self.count += 1
                    
                if rand[i] == 4: 
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(role[0], 1)} 되면 누구에게 가보고 싶니?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(role[0], 1)} 되면 누구에게 가보고 싶니?",
                                               pos_bhv="do_question_S", pos="가서 무엇을 하고 싶니?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어.",
                                               act_bhv="do_questino_S", act="가서 무엇을 하고 싶니?")
                    
                    if answer[0][0] == "positive" or answer[0][0] =="action":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q="함께 어디로 가고 싶니?",
                                                   neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어..",)             
                    self.count += 1
                    
                if rand[i] == 5: 
                    pibo = cm.tts(bhv="do_explain_A", string=f"파이보는 {wm.word(role[0], 1)} 되면 구름 위에 집을 짓고 싶어.")
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(role[0], 1)} 되면 어디에 집을 짓고 싶니?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(role[0], 1)} 되면 어디에 집을 짓고 싶니?",
                                               pos_bhv="do_question_S", pos="어떤 모양의 집을 짓고 싶니?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 상상하기 어려울 수 있어.",
                                               act_bhv="do_question_S", act="어떤 모양의 집을 짓고 싶니?")
                    
                    if answer[0][0] == "positive" or answer[0][0] =="action":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q="어떤 모양의 집을 짓고 싶니?",
                                                   pos_bhv="do_compliment_S", pos="그럼 정말 좋겟다.",
                                                   neu_bhv="do_compliment_S", neu="괜찮아. 상상하기 어려울 수 있어.",
                                                   act_bhv="do_compliment_S", act=" 그럼 정말 좋겠다.")      
                    self.count += 1
                    
                if rand[i] == 6: 
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(role[0], 1)} 되면 얼마나 높이 날아보고 싶니? ")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}는 {wm.word(role[0], 2)} 되어서 몰래 도와주고 싶은 사람이 있니?",
                                               pos_bhv="do_question_S", pos="그 곳에 가면 무엇이 있을까?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 상상하기 어려울 수 있어.",
                                               act_bhv="do_question_S", act="그 곳에 가면 무엇이 있을까?")
                    
                    if answer[0][0] == "positive" or answer[0][0] =="action":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q="그 곳에 가면 무엇이 있을까?",
                                                   neu_bhv="do_compliment_S", neu="괜찮아. 상상하기 어려울 수 있어.",
                                                   act_bhv="do_compliment_S", act="정말 멋지겠는 걸?")
                    self.count += 1
            
            if self.count < 3:
                print(self.count)
                continue
            
            elif self.count == 3:
                print(self.count)
                break
        
        # 4. 마무리 대화
        pibo = cm.tts(bhv="do_joy_A", string=f"자유롭게 하늘을 나는 {wm.word(role[0], 2)} 정말 멋진 것 같아! \
               오늘은 {wm.word(self.user_name, 0)}가 하늘을 훨훨 나는 꿈을 꿨으면 좋겠다. 다음에 또 재미있는 역할놀이 하자.")




        # 3. 피드백 수집
        time.sleep(1)                   
        pibo = cm.tts(bhv="do_question_S", string="파이보랑 얘기한 거 재미있었어? 재밌었는지, 별로였는지 얘기해줄래?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"파이보랑 얘기한 거 재미있었어?")

        pibo = cm.tts(bhv="do_joy_A", string=f"나랑 놀아줘서 고마워.") 
              
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
    rop.Flying()