# -*- coding: utf-8 -*-

# 역할놀이-날씨를 나타내는 존재

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


class Roleplay():    
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = config['user_name'] 
        self.role = []
        self.count = 0
        self.score = []
        self.turns = []
        self.reject = []
        
    
    def Weather(self):
        
        # 1. 역할 알림
        pibo = cm.tts(bhv="do_suggestion_S", string="역할 놀이를 해볼까?")
        pibo = cm.tts(bhv="do_suggestion_S", string="오늘은 날씨 역할을 해보자. ") 
        
        # 2. 역할 놀이 (1 of 4)
        weather = (['하늘에 떠 있는 뜨거운 해', '기지개를 피면서 해가 뜨는 모습을 표현해', '맑은 날씨', '하늘에 해가 떴다!', '해가 떠서 세상이 따듯해졌어.'],
                  ['하늘에서 내리는 비', '손가락으로 비가 내리는 모습을 흉내내','비오는 날씨', '하늘에서 비가 내린다!', '비가 와서 세상이 추워졌어.'],
                  ['하늘의 천둥이', '박수를 치면서 천둥을 흉내내', '천둥치는 날씨', '하늘에서 천둥이 친다!', '천둥이 쳐서 세상이 어두워졌어.'],
                  ['하늘의 바람이', '입으로 바람을 불면서 바람을 흉내내', '바람부는 날씨', '하늘에서 바람이 분다!', '바람이 불어서 세상이 시원해졌어.'])

        role = random.choice([weather[0], weather[1], weather[2], weather[3]])
        
        if role == weather[0]: self.role = ['해', '해가 뜬 맑은']
        if role == weather[1]: self.role = ['비', '비가 오는']
        if role == weather[2]: self.role = ['천둥', '천둥이 치는']
        if role == weather[3]: self.role = ['바람', '바람이 부는']                
        
        pibo = cm.tts(bhv="do_explain_A", string=f"이제 우리는 {role[0]}야!")
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"{role[1]}보자! 시이작!")
        answer = cm.responses_proc(re_bhv="do_suggestion_S", re_q=f"{role[1]}보자! 시이작!",
                                   neu_bhv="do_explain_B", neu=f"내가 {role[2]}를 들려줄게!",
                                   act_bhv="do_joy_A", act=f"{role[3]}")
        
        pibo = cm.tts(bhv="do_compliment_S", string=f"{role[4]}")
        
        # 대화 시작 (3 of 7)
        rand = random.sample(range(1,7), 3)
        
        while True:
            for i in range(len(rand)):
                
                if rand[i] == 1:                             
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 {wm.word(self.role[0], 1)} 된다면 어디에 가고 싶니?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}는 {wm.word(self.role[0], 1)} 된다면 어디에 가고 싶니?",
                                               pos_bhv="do_question_S", pos="또 어디에 가고 싶니?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 바로 떠오르지 않을 수 있어.",
                                               act_bhv="do_question_S", act=f"또 어디에 가고 싶니?")                    
                    
                    if answer[0][0] == "positive" or answer[0][0] == "action":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"또 어디에 가고 싶니?",
                                                   neu_bhv="do_compliment_S", neu="괜찮아. 바로 생각 나지 않을 수 있어.")
                                            
                    self.count += 1 

                if rand[i] == 2:                             
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 {wm.word(self.role[0], 1)} 된다면 누구한테 가고 싶니?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}는 {wm.word(self.role[0], 1)} 된다면 누구한테 가고 싶니?",
                                               pos_bhv="do_question_S", pos="가서 무엇을 하고 싶니?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 바로 떠오르지 않을 수 있어.",
                                               act_bhv="do_question_S", act=f"가서 무엇을 하고 싶니?")                    
                    
                    if answer[0][0] == "positive" or answer[0][0] == "action":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"가서 무엇을 하고 싶니?",
                                                   neu_bhv="do_compliment_S", neu="괜찮아. 바로 생각 나지 않을 수 있어.")
                                                         
                    self.count += 1 

                if rand[i] == 3:                             
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.role[0], 1)}가 되어 {wm.word(self.user_name, 0)} 집으로 가보자. {wm.word(self.user_name, 0)}는 {self.role[1]} 날씨에 무엇을 하고 있을까?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.role[0], 1)}가 되어 {wm.word(self.user_name, 0)} 집으로 가보자. {wm.word(self.user_name, 0)}는 {self.role[1]} 날씨에 무엇을 하고 있을까?",
                                               pos_bhv="do_question_S", pos=f"{wm.word(self.user_name, 0)} 기분은 어떨까?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 상상하기 어려울 수 있어.",
                                               act_bhv="do_question_S", act=f"{wm.word(self.user_name, 0)} 기분은 어떨까?")                    
                    
                    if answer[0][0] == "positive" or answer[0][0] == "action":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)} 기분은 어떨까?",
                                                   neu_bhv="do_compliment_S", neu=f"괜찮아. 바로 생각 나지 않을 수 있어.",
                                                   act_bhv="do_compliment_S", act=f"그런 기분이구나!")
                                                             
                    self.count += 1 

                if rand[i] == 4:                             
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.role[0], 2)} 누구에게 가장 필요할까?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.role[0], 2)} 누구에게 가장 필요할까?",
                                               pos_bhv="do_question_S", pos=f"{wm.word(self.user_name, 0)}도 {wm.word(self.role[0], 1)} 필요할 때가 있었니?",
                                               neu_bhv="do_compliment_S", neu="몰라도 괜찮아.",
                                               act_bhv="do_question_S", act=f"{wm.word(self.user_name, 0)}도 {wm.word(self.role[0], 1)} 필요할 때가 있었니?")                    
                    
                    if answer[0][0] == "positive" or answer[0][0] == "action":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}도 {wm.word(self.role[0], 1)} 필요할 때가 있었니?",
                                                   neu_bhv="do_compliment_S", neu="몰라도 괜찮아.")
                                                           
                    self.count += 1 

                if rand[i] == 5:                             
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 {wm.word(self.role[1], 1)} 날씨에 기분이 어때?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}는 {wm.word(self.role[1], 1)} 날씨에 기분이 어때?",
                                               pos_bhv="do_question_S", pos="그럴 때 무엇을 하고 싶니?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어.",
                                               act_bhv="do_question_S", act=f"그럴 때 무엇을 하고 싶니?")                    
                    
                    if answer[0][0] == "positive" or answer[0][0] == "action":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"그럴 때 무엇을 하고 싶니?",
                                                   neu_bhv="do_compliment_S", neu="괜찮아. 바로 생각 나지 않을 수 있어.")
                                                              
                    self.count += 1 

                if rand[i] == 6:                             
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 {wm.word(self.role[1], 1)} 날씨에 누가 생각나니?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, 0)}는 {wm.word(self.role[1], 1)} 날씨에 누가 생각나니?",
                                               pos_bhv="do_question_S", pos="함께 하고 싶은게 있니?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 바로 떠오르지 않을 수 있어.",
                                               act_bhv="do_question_S", act=f"함께 하고 싶은게 있니?")                    
                    
                    if answer[0][0] == "positive" or answer[0][0] == "action":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"함께 하고 싶은게 있니?",
                                                   neu_bhv="do_compliment_S", neu="괜찮아. 대답하기 어려울 수 있어.")
                                                         
                    self.count += 1 

                if rand[i] == 7:                             
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.role[1], 1)} 날씨는 어떤 계절에 가장 많이 나타날까?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.role[1], 1)} 날씨는 어떤 계절에 가장 많이 나타날까?",
                                               pos_bhv="do_question_S", pos=f"{wm.word(self.user_name, 0)}는 어떤 계절을 좋아하니?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 바로 떠오르지 않을 수 있어.",
                                               act_bhv="do_question_S", act=f"{wm.word(self.user_name, 0)}는 어떤 계절을 좋아하니?")                    
                    
                    if answer[0][0] == "positive" or answer[0][0] == "action":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 어떤 계절을 좋아하니?",
                                                   pos_bhv="do_question_S", pos=f"그 계절에는 무엇을 하면 재미있니?",
                                                   neu_bhv="do_compliment_S", neu="괜찮아. 바로 생각 나지 않을 수 있어.",
                                                   act_bhv="do_question_S", act="그 계절에는 무엇을 하면 재미있니?")
                        
                        if answer[0][0] == "positive" or answer[0][0] == "action":
                            answer = cm.responses_proc(re_bhv="do_question_S", re_q="그 계절에는 무엇을 하면 재미있니?",
                                                       pos_bhv="do_joy_B", pos="생각만 해도 좋은 걸?",
                                                       neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어.",
                                                       act_bhv="do_joy_B", act="생각만 해도 좋은 걸?")
                                                               
                    self.count += 1 

            if self.count < 3:
                print(self.count)
                continue
            
            elif self.count == 3:
                print(self.count)
                break
        
        # 4. 마무리 대화
        pibo = cm.tts(bhv="do_joy_A", string=f"직접 날씨가 되어보니 신기한 걸? {self.role[0]} 역할을 정말 잘 해줬어! 다음에 또 재미있는 역할놀이 하자.")




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
    rop.Weather()