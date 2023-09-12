# -*- coding: utf-8 -*-

# 역할놀이-가상 캐릭터

import os, sys
import re
import time
import json
from datetime import datetime 
import random
import csv

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
        self.genre = ''
        self.fav=''
        self.count = 0
        self.score = []
        self.turns = []
        self.reject = []
        
    
    def Character(self):
        
        # 1. 역할 알림
        pibo = cm.tts(bhv="do_suggestion_S", string="역할 놀이를 해볼까?")
        pibo = cm.tts(bhv="do_suggestion_S", string=f"오늘은 {wm.word(self.user_name, 0)}가 좋아하는 캐릭터 역할 놀이를 해볼거야.") 
                
        # 2. 역할 놀이 (1 of 3)
        genre_list = ['만화', '영화', '동화']        
        self.genre = random.choice(genre_list)
        
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 어떤 {wm.word(self.genre, 3)} 제일 좋아하니?")        
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 어떤 {wm.word(self.genre, 3)} 제일 좋아하니?")

        while True:     # 다른 옵션으로 질문
            if answer[0][0] == "action" or answer[0]=="positive":                
                break
            
            if answer[0][0] == "neutral" or answer[0]=="negative":
                genre_list.remove(self.genre)
                self.genre = random.choice(genre_list)
                
                pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, 0)}는 어떤 {wm.word(self.genre, 3)} 제일 좋아하니?")     
                answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 어떤 {wm.word(self.genre, 3)} 제일 좋아하니?")   
                        
                continue
        
        pibo = cm.tts(bhv="do_question_L", string=f"그 {self.genre} 속에서 {wm.word(self.user_name, 0)}는 누가 제일 마음에 드니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"그 {self.genre} 속에서 {wm.word(self.user_name, 0)}는 누가 제일 마음에 드니?")
        
        if answer[0][0] == "action":
            self.fav = answer[1]
            # pibo = cm.tts(bhv="do_question_L", string=f"그 {self.genre} 속에서 {wm.word(self.user_name, 0)}는 누가 제일 마음에 드니?")
            # answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"그 {self.genre} 속에서 {wm.word(self.user_name, 0)}는 누가 제일 마음에 드니?") 
            
            pibo = cm.tts(bhv="do_question_S", string=f"{self.fav} 맞니?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{self.fav}맞니?",
                                       pos_bhv="do_question_S", pos=f"{self.fav}의 특징을 한번 흉내내볼래?",
                                       neu_bhv="do_question_S", neu="이름을 다시 말해 줄래?",
                                       neg_bhv="do_question_S", neg="이름을 다시 말해 줄래?")
            
            while True:
                if answer[0][0] == "positive":                    
                    break
                
                if answer[0] != "positive":
                    # answer = cm.responses_proc(re_bhv="do_question_S", re_q="이름을 다시 말해 줄래?")
                    pibo = cm.tts(bhv="do_question_S", string=f"{answer[1]}맞니?")
                    continue
        
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{self.fav}의 특징을 한번 흉내내볼래?",
                                   neu_bhv="do_compliment_S", neu="몰라도 괜찮아.",
                                   act_bhv="do_joy_A", act="정말 멋진 캐릭터구나!")
        
        # 3. 대화 시작 (3 of 6)     
        rand = random.sample(range(1,5), 3)     # 질문이 4개임
        
        while True:
            for i in range(len(rand)):
                if rand[i] == 1:
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.fav, 1)} 제일 멋있다고 생각할 때가 언제니?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.fav, 1)} 제일 멋있다고 생각할 때가 언제니?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어.",
                                               act_bhv="do_question_S", act="어떤 장면이었는지 자세히 말해줄래?")        
                    
                    if answer[0][0] == "action":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q="어떤 장면이었는지 자세히 말해줄래?",
                                                   neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어")
                    self.count += 1 
                    
                if rand[i] == 2: 
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.fav, 2)} {self.genre} 에서 누구와 제일 친하니?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.fav, 2)} {self.genre} 에서 누구와 제일 친하니?",
                                               neu_bhv="do_compliment_S", neu="몰라도 괜찮아.")
                    
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 누구랑 제일 친해?")
                    answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 누구랑 제일 친해?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어.")
                    self.count += 1
                    
                if rand[i] == 3: 
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.fav, 1)} 된다면 {wm.word(self.user_name, 0)}는 어떤 것을 해보고 싶니?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.fav, 1)} 된다면 {wm.word(self.user_name, 0)}는 어떤 것을 해보고 싶니?",
                                               pos_bhv="do_question_S", pos="언제 그걸 해보고 싶니?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 상상하기 어려울 수 있어.",
                                               act_bhv="do_question_S", act="언제 그걸 해보고 싶니?")
                    
                    if answer[0][0] == "positive" or answer[0][0] =="action":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q="언제 그걸 해보고 싶니?",
                                                   neu_bhv="do_compliment_S", neu="괜찮아. 상상하기 어려울 수 있어.")
                    self.count += 1
                    
                if rand[i] == 4: 
                    pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.fav, 5)} 비슷하게 생긴 사람이 주변에 있니?")
                    answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.fav, 5)} 비슷하게 생긴 사람이 주변에 있니?",
                                               pos_bhv="do_question_S", pos="그 사람은 어떻게 생겼니?",
                                               neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어.",
                                               act_bhv="do_questino_S", act="그 사람은 어떻게 생겼니?")
                    
                    if answer[0][0] == "positive" or answer[0][0] =="action":
                        answer = cm.responses_proc(re_bhv="do_question_S", re_q="그 사람은 어떻게 생겼니?",
                                                   neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어..",
                                                   act_bhv="do_question_S", act=f"그 사람을 만나면 {wm.word(self.user_name, 0)}는 기분이 어때?")             
                        
                        if answer[0][0] =="action":
                            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"그 사람을 만나면 {wm.word(self.user_name, 0)}는 기분이 어때?",
                                                       pos_bhv="do_joy_B", pos="정말 신기할 것 같아!",
                                                       neu_bhv="do_compliment_S", neu="괜찮아. 대답하기 어려울 수 있어")        
                    self.count += 1
                            
            if self.count < 3:
                print(self.count)
                continue
            
            elif self.count == 3:
                print(self.count)
                break
        
        # 4. 마무리 대화
        pibo = cm.tts(bhv="do_joy_B", string=f"{wm.word(self.user_name, 0)}와 캐릭터 이야기를 해서 너무 재미있었어. 다음에 또 재미있는 역할놀이 하자.")




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
    rop.Character()