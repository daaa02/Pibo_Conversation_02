# -*- coding: utf-8 -*-

# 일상-기념일 대화

import os, sys
import re
import csv
import random
from datetime import datetime
import time
import json
from datetime import date

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


class Daily():    
    
    def __init__(self): 
        self.user_name = '다영'
        self.this_year = date.today().year
        self.dob_child = [1998, 10, 2]    # 나중엔 사용자 DB에서 참조하도록
        self.age_child = (self.this_year-self.dob_child[0]) + 1
        self.dob_parent = [['엄마', 1998, 10, 2], []]
    
    
    def Bday(self):   
        
        # 1.1 기념일 알림
        audio.audio_play(filename="/home/pi/Pibo_Conversation/data/behavior/audio/sound_cheerfulness2.wav", out='local', volume=-1500, background=False)
        pibo = cm.tts(bhv="do_joy_A", string=f"3일 뒤 {wm.word(self.user_name, type=0)} 생일이지?")
        answer = cm.responses_proc(re_bhv="do_joy_A", re_q=f"3일 뒤 {wm.word(self.user_name, type=0)} 생일이지?",
                                   pos_bhv="do_joy_A", pos=f"{wm.word(self.user_name, type=0)}가 벌써 {self.age_child}살이 되는 구나!",
                                   act_bhv="do_joy_A", act=f"{wm.word(self.user_name, type=0)}가 벌써 {self.age_child}살이 되는 구나!")
        
        # 1.2 대화 시작
        pibo = cm.tts(bhv="do_question_S", string="이번 생일에는 뭘 하고 싶어?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="이번 생일에는 뭘 하고 싶어?",
                                   pos_bhv="do_joy_B", pos=f"{wm.word(self.user_name, type=0)} 생일이어서 행복할 것 같아! 받고 싶은 선물이 있다면 말해 볼래?",
                                   neu_bhv="do_question_S", neu="받고 싶은 선물이 있다면 말해 볼래?",
                                   neg_bhv="do_question_S", neg="받고 싶은 선물이 있다면 말해 볼래?",
                                   act_bhv="do_joy_B", act=f"{wm.word(self.user_name, type=0)} 생일이어서 행복할 것 같아! 받고 싶은 선물이 있다면 말해 볼래?")
        
        if answer[0][0] == "positive" or answer[0][0] =="action":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="받고 싶은 선물이 있다면 말해 볼래?",
                                       pos_bhv="do_joy_A", pos="그걸 선물로 받으면 좋겠는 걸! 또 받고 싶은 선물 있어?",
                                       act_bhv="do_joy_A", act="그걸 선물로 받으면 좋겠는 걸! 또 받고 싶은 선물 있어?")
            
            answer = cm.responses_proc(re_bhv="do_joy_A", re_q="또 받고 싶은 선물 있어?",
                                       pos_bhv="do_joy_B", pos="그걸 선물로 받으면 좋겠는 걸!",
                                       act_bhv="do_joy_B", act="그걸 선물로 받으면 좋겠는 걸!")
            
            # 나중에 받고 싶은 선물 저장 기능 추가
            # present = []
            # present.append()
            
        pibo = cm.tts(bhv="do_question_L", string=f"난 초코 케잌을 좋아하는데, {wm.word(self.user_name, 0)}는 어떤 케이크를 좋아 하니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"난 초코 케잌을 좋아하는데, {wm.word(self.user_name, 0)}는 어떤 케이크를 좋아 하니?",
                                   pos_bhv="do_suggestion_L", pos="정말 맛있겠는걸! 이번 생일날 먹고 싶다고 부모님께 이야기해볼래?",
                                   act_bhv="do_suggestion_L", act="정말 맛있겠는걸! 이번 생일날 먹고 싶다고 부모님께 이야기해볼래?")
        
        if answer[0][0] == "positive" or answer[0][0] =="action":
            answer = cm.responses_proc(re_bhv="do_suggestion_L", re_q="정말 맛있겠는걸! 이번 생일날 먹고 싶다고 부모님께 이야기해볼래?",
                                       pos_bhv="do_joy_A", pos="부모님이 정말 사주실지도 몰라!",
                                       act_bhv="do_joy_A", act="부모님이 정말 사주실지도 몰라!")
        
        pibo = cm.tts(bhv="do_suggestion_S", string=f"파이보도 {wm.word(self.user_name, 0)} 생일 파티에 초대해줄 수 있어?")
        answer = cm.responses_proc(re_bhv="do_suggestion_S", re_q=f"파이보도 {wm.word(self.user_name, 0)} 생일 파티에 초대해줄 수 있어?",
                                   pos_bhv="do_joy_B", pos=f"고마워. 파이보가 행복한 {wm.word(self.user_name, 0)} 모습을 사진 찍어줄게!")
        
        pibo = cm.tts(bhv="do_joy_A", string=f"행복하고 기분 좋은 생일을 보냈으면 좋겠어! {wm.word(self.user_name, 0)} 생일에 나도 특별히 생일 노래를 불러줄게! 기대해도 좋아.")     
                                   
                                   
    def Bday_Parent(self):   # 나중엔 엄마/아빠 생일 중 하나만 있어도 되게끔
        
        # 1.1 기념일 알림
        # audio.audio_play(filename="/home/pi/AI_pibo2/src/data/audio/**")
        pibo = cm.tts(bhv="do_joy_A", string=f"3일 뒤 {self.dob_parent[0][0]} 생일이지?")
        answer = cm.responses_proc(re_bhv="do_joy_A", re_q=f"",
                                   pos_bhv="do_question_S", pos=f"이번 {self.dob_parent[0][0]}생일에는 어떻게 축하드리면 좋을까?",
                                   neu_bhv="do_question_S", neu=f"괜찮아. 파이보가 알려주면 되지. 이번 {self.dob_parent[0][0]}생일에는 어떻게 축하드리면 좋을까?",
                                   neg_bhv="do_question_S", neg=f"괜찮아. 이번 {self.dob_parent[0][0]}생일에는 어떻게 축하드리면 좋을까?")
        
        # positive 아닌 경우에 바로 대화 끝나는 게 맞나 싶어서 그냥 이어서 함
        answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"이번 {self.dob_parent[0][0]}생일에는 어떻게 축하드리면 좋을까?",
                                   pos_bhv="so_compliment_S", pos="정말 좋은 생각인 것 같아!",
                                   neg_bhv="do_question_S", neg="어떤 선물을 좋아하실까?",
                                   act_bhv="so_compliment_S", act="정말 좋은 생각인 것 같아!")
        
        if answer[0][0] == "negative":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"어떤 선물을 좋아하실까?",
                                       pos_bhv="do_suggestion_S", pos=f"엄마는 {wm.word(self.user_name, 0)}가 편지를 써 드려도 정말 기뻐하실거야!",
                                       neu_bhv="do_suggestion_S", neu=f"엄마는 {wm.word(self.user_name, 0)}가 편지를 써 드려도 정말 기뻐하실거야!",
                                       act_bhv="do_suggestion_S", act=f"엄마는 {wm.word(self.user_name, 0)}가 편지를 써 드려도 정말 기뻐하실거야!")

        pibo = cm.tts(bhv="do_suggestion_L", string="영상 편지를 찍어보면 어때? 엄마 생일 축하 영상으로 말이야. 내가 동영상 찍어줄 수 있는데 지금 해볼래?")                                    
        answer = cm.responses_proc(re_bhv="do_suggestion_S", re_q="내가 동영상 찍어줄 수 있는데 지금 해볼래?",
                                   pos_bhv="do_waiting_A", pos="좋아! 준비가 되면 준비 됐다고 말해줘.",
                                   neu_bhv="do_explain_B", neu="그럼 다음에 찍어 드리자!",
                                   neg_bhv="do_explain_B", neg="그럼 다음에 찍어 드리자!")
        
        if answer[0][0] == "positive":
            cm.responses_proc(re_bhv="do_waiting_A", re_q="좋아! 준비가 되면 준비 됐다고 말해줘.",
                              pos_bhv="do_photo", pos="편지가 모두 끝나면 끝났다고 말해줘. 찍는다 하나, 둘, 셋!")   # 말하고 사진 동작해야할 듯. 순서 다시 봐야함
            
            # 영상 촬영 중단하는 신호 추가 필요
            cm.responses_proc(act_bhv="do_joy_A", act=f"정말 잘 하는 걸? {wm.word(self.dob_parent[0][0], 1)} 너무 좋아하실 것 같아")
        
        pibo = cm.tts(bhv="do_joy_B", string="엄마 생일날 파이보와 함께 축하해드리자!")
        
        
    def ChildrensDay(self):
        
        # 1.1 기념일 알림
        # audio.audio_play(filename="/home/pi/AI_pibo2/src/data/audio/**")
        pibo = cm.tts(bhv="do_joy_A", string="3일 뒤 어린이날이야!")
        answer = cm.responses_proc(re_bhv="do_joy_A", re_q="3일 뒤 어린이날이야!",
                                   pos_bhv="do_joy_A", pos="어린이 날이라 기쁠 것 같아!")
        
        # 1.2 대화 시작
        pibo = cm.tts(bhv="do_question_S", string="받고 싶은 선물이 있다면 말해 볼래?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="받고 싶은 선물이 있다면 말해 볼래?",
                                   pos_bhv="do_joy_B", pos="그걸 선물로 받으면 좋겠는 걸!",
                                   act_bhv="do_joy_B", act="그걸 선물로 받으면 좋겠는 걸!")
            
        pibo = cm.tts(bhv="do_question_S", string="이번 어린이날에 어디 가고 싶은 곳이 있니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="이번 어린이 날에 어디 가고 싶은 곳이 있니?",
                                   pos_bhv="do_question_S", pos="어디로 가보고 싶어?",
                                   neu_bhv="do_question_S", neu="어디 가고 싶은 곳 없어?")
        
        if answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="어디로 가보고 싶어?")
            
            pibo = cm.tts(bhv="do_question_S", string="거기 가서 뭐 하고 싶니?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="거기 가서 뭐 하고 싶니?",
                                       pos_bhv="do_joy_A", pos="그 곳에 가면 정말 재밌겠는걸!",
                                       neu_bhv="do_compliment_S", neu="그럴 수 있지. 나도 집에서 쉬고 싶을 때도 있어!",
                                       act_bhv="do_joy_A", act="그 곳에 가면 정말 재밌겠는걸!")
        
        pibo = cm.tts(bhv="do_explain_A", string="어린이날은 어린이들이 씩씩하고 올바르게 자라도록 나라에서 정한 날이야! 알고 있었니?")
        answer = cm.responses_proc(re_bhv="do_explain_A", re_q="어린이날은 어린이들이 씩씩하고 올바르게 자라도록 나라에서 정한 날이야! 알고 있었니?",
                                   pos_bhv="do_compliment_S", pos="정말 대단한 걸?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 파이보가 알려줬잖아.",
                                   act_bhv="do_compliment_S", act="괜찮아. 파이보가 알려줬잖아.")
        
        pibo = cm.tts(bhv="do_joy_A", string=f"{wm.word(self.user_name, type=0)}가 정말 행복한 어린이날을 보냈으면 좋겠어!")
        
        pibo = cm.tts(bhv="do_joy_B", string="이번 어린이날에도 즐겁게 놀고 더 씩씩하고 건강한 어린이가 되자!")
        
        
    def ParentsDay(self):
        
        # 1.1 기념일 알림
        # audio.audio_play(filename="/home/pi/AI_pibo2/src/data/audio/**")
        pibo = cm.tts(bhv="do_joy_A", string="3일이 지나면 어버이날이네!")
        
        pibo = cm.tts(bhv="do_question_L", string=f"어버이날에는 보통 카네이션이랑 편지를 드린다고 하던데, {wm.word(self.user_name, type=0)}도 드려본 적 있어?")
        
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="카네이션이랑 편지를 부모님께 드려본 적 있어?",
                                   pos_bhv="do_question_S", pos="어디서 카네이션을 만들어서 부모님께 드렸니?")
        
        if answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="어디서 카네이션을 만들어서 부모님께 드렸니?",
                                       pos_bhv="do_joy_A", pos="정말 좋아하셨겠다!",
                                       act_bhv="do_joy_A", act="정말 좋아하셨겠다!")
            
        pibo = cm.tts(bhv="do_explain_A", string="어버이날은 나를 낳아주신 부모님과 할머니, 할아버지께 감사하는 날이야. 알고 있었니?")
        answer = cm.responses_proc(re_bhv="do_explain_A", re_q="어버이날은 나를 낳아주신 부모님과 할머니, 할아버지께 감사하는 날이야. 알고 있었니?",
                                   pos_bhv="do_compliment_S", pos="정말 대단한 걸?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 파이보가 알려줬잖아.",
                                   act_bhv="do_compliment_S", act="괜찮아. 파이보가 알려줬잖아.")
                                   
        pibo = cm.tts(bhv="do_suggestion_L", string="이번 어버이날에는 부모님께 어버이날 노래도 불러드리면 어떨까? 내가 동영상 찍어 줄 수 있어!")                                    
        answer = cm.responses_proc(re_bhv="do_suggestion_S", re_q="내가 동영상 찍어줄 수 있는데 지금 해볼래?",
                                   pos_bhv="do_waiting_A", pos="좋아! 준비가 되면 준비 됐다고 말해줘.",
                                   neu_bhv="do_explain_B", neu="그럼 다음에 찍어 드리자!",
                                   neg_bhv="do_explain_B", neg="그럼 다음에 찍어 드리자!")
        
        if answer[0][0] == "positive":
            cm.responses_proc(re_bhv="do_waiting_A", re_q="좋아! 준비가 되면 준비 됐다고 말해줘.",
                              pos_bhv="do_photo", pos="노래가 끝나면 노래 끝! 이라고 말해줘. 찍는다 하나, 둘, 셋!")   # 말하고 사진 동작해야할 듯. 순서 다시 봐야함
            
            # 영상 촬영 중단하는 신호 추가 필요
            cm.responses_proc(act_bhv="do_joy_A", act=f"정말 잘하는 걸? 부모님께서 너무 좋아하실 것 같아!")
        
        pibo = cm.tts(bhv="do_joy_B", string="어버이날에 내가 가족사진도 멋지게 찍어줄게! 기대해.")
    
    
    def Christmas(self):
        
        # 1.1 기념일 알림
        # audio.audio_play(filename="/home/pi/AI_pibo2/src/data/audio/**")
        pibo = cm.tts(bhv="do_joy_A", string="3밤만 자면 크리스마스야!")
        
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, type=0)}가 좋아하는 크리스마스 캐롤이 뭔지 말해줄래?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, type=0)}가 좋아하는 크리스마스 캐롤이 뭔지 말해줄래?",
                                   pos_bhv="do_joy_A", pos="캐롤은 기분을 좋게 만들어주는 마법 같아.",
                                   neu_bhv="do_compliment_S", neu="그럴 수 있지.",
                                   act_bhv="do_joy_A", act="캐롤은 기분을 좋게 만들어주는 마법 같아.")
        
        pibo = cm.tts(bhv="do_question_S", string="최근에 멋진 크리스마스 트리를 본 적이 있니?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="최근에 멋진 크리스마스 트리를 본 적이 있니?",
                                   pos_bhv="do_question_S", pos="어디서 봤니?")
        
        if answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="어디서 봤니?",
                                       pos_bhv="do_joy_B", pos="크리스마스 트리는 반짝반짝 너무 이쁜 것 같아.",
                                       neu_bhv="do_compliment_S", neu="그럴 수 있지.",
                                       act_bhv="do_joy_B", act="크리스마스 트리는 반짝반짝 너무 이쁜 것 같아!")
    
        pibo = cm.tts(bhv="do_question_S", string="이번 크리스마스에 멋진 계획이 있다면 말해 줄래?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="이번 크리스마스에 멋진 계획이 있다면 말해 줄래?",
                                   pos_bhv="do_joy_B", pos="와. 멋진 크리스마스가 될 수 있겠는 걸?",
                                   act_bhv="do_joy_B", act="와. 멋진 크리스마스가 될 수 있겠는 걸?")
        
        pibo = cm.tts(bhv="do_question_S", string="크리스마스에 받고 싶은 선물이 있다면 알려줄래?")
        answer = cm.responses_proc(re_bhv="do_question_S", re_q="크리스마스에 받고 싶은 선물이 있다면 알려줄래?")
        
        pibo = cm.tts(bhv="do_joy_A", string=f"{wm.word(self.user_name, type=0)}가 행복하고 멋진 크리스마스를 보냈으면 좋겠어!")

        pibo = cm.tts(bhv="do_joy_B", string="크리스마스에 내가 멋진 캐롤을 들려줄게. 기대해!")
        
        
        
        
if __name__ == "__main__":
    day = Daily()
    day.Bday()