# -*- coding: utf-8 -*-

# 역할 놀이-되고 싶은 인물

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


class RolePlay():    
    
    def __init__(self): 
        with open('/home/pi/name_config.json', 'r') as f:
            config = json.load(f)        
            self.user_name = config['user_name'] 
        self.rolemodel = ''
        self.score = []
        self.turns = []
        self.reject = []
        

    def RoleModel(self):
        
        # 1.1 역할 알림
        pibo = cm.tts(bhv="do_question_S", string=f"역할 놀이를 해볼까? {wm.word(self.user_name, type=0)}가 원하는 사람이 되어볼거야!")
        
        # 2.1 역할놀이(1)
        pibo = cm.tts(bhv="do_question_L", string=f"파이보는 커서 과학자가 되고 싶어! {wm.word(self.user_name, type=0)}는 뭐가 되고 싶니?")
        
        while True:
            answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, type=0)}는 뭐가 되고 싶니?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "neutral":
                pibo = cm.tts(bhv="do_explain_B", string=f"괜찮아. 바로 떠오르지 않을 수도 있어. 소방관, 의사, 디자이너, 화가 등이 있어. {wm.word(self.user_name, type=0)}는 뭐가 되고 싶니?")
                answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, type=0)}는 뭐가 되고 싶니?")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
                
                if answer[0][0] == "neutral" or answer [0][0] == "negative":
                    self.rolemodel = "과학자"
                    pibo = cm.tts(bhv="do_explain_A", string=f"그럼 파이보가 되고 싶은 과학자 얘기를 하자!")
                    break
                
                if answer[0][0] == "positive" or answer[0][0] == "action":
                    self.rolemodel = nlp.nlp_nouns(answer[0][1])   # NER

                    pibo = cm.tts(bhv="do_question_S", string=f"{self.rolemodel} 맞아?")
                    answer = cm.responses_proc(re_q=f"{self.rolemodel} 맞아?")
                    cwc.writerow(['pibo', pibo])
                    cwc.writerow(['user', answer[0][1], answer[1]])
                    self.reject.append(answer[1])
                    
                    if answer[0][0] == "negative":
                        pibo = cm.tts(bhv="do_question_S", string=f"다시 크게 말해줄래?")
                        continue
                
                    else:
                        break  
                                
            
            if answer[0][0] == "positive" or answer[0][0] == "action":
                self.rolemodel = nlp.nlp_nouns(answer[0][1])   # NER
                
                pibo = cm.tts(bhv="do_question_S", string=f"{self.rolemodel} 맞아?")
                answer = cm.responses_proc(re_q=f"{self.rolemodel} 맞아?")
                
                if answer[0][0] == "negative":
                    pibo = cm.tts(bhv="do_question_S", string=f"다시 크게 말해줄래?")
                    continue
                
                else:
                    break
        
        # 3.1 역할 대화
        pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.rolemodel, type=2)} 정말 중요한 일을 한다고 생각해.")
        
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, type=0)}는 가장 유명한 {wm.word(self.rolemodel, type=3)} 아니?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, type=0)}는 가장 유명한 {wm.word(self.rolemodel, type=3)} 아니?",
                                   neu_bhv="do_compliment_S", neu="몰라도 괜찮아.")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
        
        if answer[0][0] == "positive" or answer[0][0] == "action":
            pibo = cm.tts(bhv="do_question_S", string=f"그 사람은 왜 유명할까?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="그 사람은 왜 유명할까?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            pibo = cm.tts(bhv="do_question_S", string=f"{wm.word(self.user_name, type=0)}의 주변에 {wm.word(self.rolemodel, type=1)} 있니?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="주변에 있니?",
                                       neu_bhv="do_compliment_S", neu="괜찮아. 생각 나지 않을 수 있어")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            if answer[0][0] == "positive":
                pibo = cm.tts(bhv="do_question_S", string=f"그 사람은 누구니?")
                answer = cm.responses_proc(re_q="그 사람은 누구니?")
                cwc.writerow(['pibo', pibo])
                cwc.writerow(['user', answer[0][1], answer[1]])
                self.reject.append(answer[1])
            
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.rolemodel, type=3)} 생각하면 무슨 색이 떠올라?")
        answer = cm.responses_proc(re_bhv="do_question_L", re_q=f"{wm.word(self.user_name, type=3)} 생각하면 무슨 색이 떠올라?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 바로 떠오르지 않을 수도 있어")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
        
        if answer[0][0] == "positive":
            pibo = cm.tts(bhv="do_question_S", string=f"그 색깔이 왜 떠올랐을까?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="그 색깔이 왜 떠올랐을까?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
            
            
        pibo = cm.tts(bhv="do_question_L", string=f"{wm.word(self.user_name, type=0)}가 {wm.word(self.rolemodel, type=1)} 된다면 뭘 하고 싶니?")
        answer = cm.responses_proc(re_q=f"{wm.word(self.rolemodel, type=1)} 된다면 뭘 하고 싶니?",
                                   neu_bhv="do_compliment_S", neu="괜찮아. 대답하기 어려울 수 있어")
        cwc.writerow(['pibo', pibo])
        cwc.writerow(['user', answer[0][1], answer[1]])
        self.reject.append(answer[1])
        
        if answer[0][0] == "positive":
            pibo = cm.tts(bhv="do_question_S", string=f"그렇게 생각한 이유는 뭐야?")
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="그렇게 생각한 이유는 뭐야?")
            cwc.writerow(['pibo', pibo])
            cwc.writerow(['user', answer[0][1], answer[1]])
            self.reject.append(answer[1])
        
        # 4.1 마무리 대화
        pibo = cm.tts(bhv="do_joy_A", string=f"{wm.word(self.user_name, type=0)}가 되고 싶은 역할 놀이를 해서 너무 재미있었어! 다음에 또 재미있는 역할놀이 하자.")
        
        
        
        
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
    rp = RolePlay()
    rp.RoleModel()