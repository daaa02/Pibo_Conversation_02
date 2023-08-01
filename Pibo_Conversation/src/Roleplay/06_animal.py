# -*- coding: utf-8 -*-

# 역할놀이-좋아하는 동물

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
            self.user_name = config['user_name'] 
        self.count = 0
        self.score = []
        self.turns = []
        self.reject = []
        
    
    def Animal(self):
        
        # 1. 역할 알림
        pibo = cm.tts(bhv="do_suggestion_S", string="역할 놀이를 해볼까?")
        pibo = cm.tts(bhv="do_suggestion_S", string="오늘은 동물 역할 놀이를 해보자. 이제부터 동물을 흉내내 볼거야.") 
                
        # 2. 역할 놀이 (1 of 5)
        ## 2.1 동물 소리
        animal = (['병아리', '돼지', '소'], ['호랑이', '고양이', '염소'], 
                  ['수탉', '오리', '말'], ['뻐꾸기', '개구리', '개'], ['늑대', '양', '모기'])
        role = random.choice([animal[0], animal[1], animal[2], animal[3], animal[4]])
        
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(role[0], 2)} 어떻게 울까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(role[0], 2)}는 어떻게 울까?",
                                   neu_bhv="do_explain_A", neu=f"내가 알려줄게! {wm.word(role[0], 2)} 이렇게 운단다.",
                                   neg_bhv="do_explain_A", neg=f"내가 알려줄게! {wm.word(role[0], 2)} 이렇게 운단다.",
                                   act_bhv="do_compliment_S", act="잘하는 걸? 파이보도 한번 따라해 볼게!")
        # audio.audio_play(filename)
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"{wm.word(role[1], 2)} 어떤 소리를 낼까?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(role[1], 2)}는 어떻게 울까?",
                                   neu_bhv="do_explain_A", neu=f"내가 알려줄게! {wm.word(role[1], 2)} 이렇게 운단다.",
                                   neg_bhv="do_explain_A", neg=f"내가 알려줄게! {wm.word(role[1], 2)} 이렇게 운단다.",
                                   act_bhv="do_compliment_S", act="잘하는 걸? 파이보도 한번 따라해 볼게!")
        # audio.audio_play(filename)
                
        pibo = cm.tts(bhv="do_question_S", string=f"이건 누구일까?")
        # audio.audio_play(filename)
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="누구일까?",
                                   neu_bhv="do_explain_A", neu=f"내가 알려줄게! {wm.word(role[2], 2)} 이렇게 운단다.",
                                   neg_bhv="do_explain_A", neg=f"내가 알려줄게! {wm.word(role[2], 2)} 이렇게 운단다.",
                                   act_bhv="do_compliment_S", act="잘하는 걸? 파이보도 한번 따라해 볼게!")
        # audio.audio_play(filename)              
        
        pibo = cm.tts(bhv="do_joy_A", string="동물을 흉내내니까 정말 재미있는 걸?")
        
        ## 2.2 동물 행동 (1 of 5)
        animal = (['펭귄', '펭귄이 걷는 모습을 따라해', '코끼리', '팔을 겹쳐서 코를 만들어', '뱀', '기어'],
                  ['개구리', '살짝 점프해', '고양이', '살금살금 걸어', '나비', '이리저리 날아다녀'], 
                  ['사자', '늠름하게 걸어', '고릴라', '두 발로 서서 가슴을 쳐', '거북이', '느릿느릿하게 걸어'], 
                  ['꽃게', '옆으로 걸어', '치타', '빠르게 움직여', '달팽이', '천천히 기어가'], 
                  ['공룡', '앞발을 만들고 걸어', '새', '날아', '스컹크', '방구를 뿡! 뀌어'])      
        
        # print(len(animal))
        role = random.choice([animal[0], animal[1], animal[2], animal[3], animal[4]])
        
        pibo = cm.tts(bhv="do_suggestion_L", string=f"{wm.word(self.user_name, 0)}가 동물을 흉내내면 내가 멋진 사진을 찍어줄게.")
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"첫 번째는 {wm.word(role[0], 0)}야. {role[1]}볼까?")
        time.sleep(1)        
        pibo = cm.tts(bhv="do_photo", string="자. 찍는다!")
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"이번엔 {role[2]} 처럼 {role[3]}보자!")
        time.sleep(1)        
        pibo = cm.tts(bhv="do_photo", string="자. 찍는다!")       
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"{wm.word(self.user_name, 0)}가 {wm.word(role[4], 1)} 되었다고 생각하고 {role[5]}보자!")
        time.sleep(1)        
        pibo = cm.tts(bhv="do_photo", string="이번에도 멋지게 찍어 줄게!")
        
        pibo = cm.tts(bhv="do_joy_A", string=f"{wm.word(self.user_name, 0)}가 표현하니까 더 재미있는 걸? 따라한 동물들은 모두 사진 찍어두었어. 나중에 확인해봐!")
        
        # 3. 대화 시작
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, 0)}는 어떤 동물을 제일 좋아하니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{wm.word(self.user_name, 0)}는 어떤 동물을 제일 좋아하니?",
                                   pos_bhv="do_compliment_S", pos="그 동물은 어떻게 생겼니?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 바로 떠오르지 않을 수 있어.",
                                   act_bhv="do_compliment_S", act="그 동물은 어떻게 생겼니?")
        
        if answer[0][0] == "positive" or answer[0][0] =="action":
             answer = cm.responses_proc(re_bhv="do_question_S", re_q="그 동물은 어떻게 생겼니?",
                                        neu_bhv="do_compliment_S", neu="몰라도 괜찮아.")
        
        
        pibo = cm.tts(bhv="do_question_L", string=f"만약 {wm.word(self.user_name, 0)}가 원하는 동물로 변신할 수 있다면 어떤 동물이 되고 싶니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"원하는 동물로 변신할 수 있다면 어떤 동물이 되고 싶니?",
                                    neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어.")        
        
        if answer[0][0] == "action":
            fav = answer[1]
            pibo = cm.tts(bhv="do_question_S", string=f"{fav} 맞니?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"{fav}맞니?",
                                        neu_bhv="do_compliment_S", neu="이름을 다시 말해 줄래?",
                                        neg_bhv="do_compliment_S", neg="이름을 다시 말해 줄래?")
            while True:
                if answer[0][0] == "positive":                    
                    break
                if answer[0] != "positive":
                    pibo = cm.tts(bhv="do_question_S", string=f"{answer[1]}맞니?")
                    continue
                
        pibo = cm.tts(bhv="do_question_L", string=f"만약 {wm.word(fav, 0)}로 변신을 하면, 어떤 점이 제일 좋을 것 같아?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"만약 {wm.word(fav, 0)}로 변신을 하면, 어떤 점이 제일 좋을 것 같아?",
                                   pos_bhv="do_compliment_S", pos="그런 점이 좋겠구나!",
                                   neu_bhv="do_compliment_S", neu="몰라도 괜찮아.")
        
        pibo = cm.tts(bhv="do_question_L", string=f"만약 {wm.word(fav, 0)}로 변신을 한 뒤, {wm.word(self.user_name, 0)}가 제일 먼저 하고 싶은 것이 있니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"만약 {wm.word(fav, 0)}로 변신을 한 뒤, {wm.word(self.user_name, 0)}가 제일 먼저 하고 싶은 것이 있니?",
                                   pos_bhv="do_compliment_S", pos="언제 하고 싶니?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 바로 떠오르지 않을 수 있어.")
        
        if answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="언제 하고 싶니?",
                                       neu_bhv="do_compliment_S", neu="괜찮아. 생각이 나지 않을 수 있어.")
        
        pibo = cm.tts(bhv="do_question_L", string=f"만약 {wm.word(fav, 0)}로 변신을 한 뒤, 만나고 싶은 사람이 있니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"만약 {wm.word(fav, 0)}로 변신을 하면, 어떤 점이 제일 좋을 것 같아?",
                                   pos_bhv="do_compliment_S", pos="만나서 무엇을 같이 하고 싶니?",
                                   neu_bhv="do_compliment_S", neu="대답하기 어려울 수 있어.")
        
        if answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="만나서 무엇을 같이 하고 싶니?",
                                       pos_bhv="do_compliment_S", pos=f"{wm.word(self.user_name, 0)}는 상상력이 대단한 걸?",
                                       neu_bhv="do_compliment_S", neu="몰라도 괜찮아.",
                                       act_bhv="do_compliment_S", act=f"{wm.word(self.user_name, 0)}는 상상력이 대단한 걸?")
            
        pibo = cm.tts(bhv="do_question_L", string="오늘 따라한 동물 중에 어떤 게 가장 웃기고 재미있었니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q="오늘 따라한 동물 중에 어떤 게 가장 웃기고 재미있었니?",
                                   pos_bhv="do_compliment_S", pos="내 생각에도 정말 재미있었어!")
        
        # 4. 마무리 대화
        pibo = cm.tts(bhv="do_joy_B", string="정말 재밌었어. 다음에도 다양한 동물들이 되어 상상의 나래를 펼쳐보자.")




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
    rop.Animal()