# 역할놀이-마법을 부리는 존재

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
            self.user_name = config['user_name'] 
        self.role = ''
        self.score = []
        self.turns = []
        self.reject = []
        
    
    def Magician(self):
        
        # 1. 역할 알림
        pibo = cm.tts(bhv="do_suggestion_S", string="역할 놀이를 해볼까?")
        pibo = cm.tts(bhv="do_suggestion_S", string="오늘은 마법 주문을 걸어보자.")
        
        # 2. 역할 놀이 (1 of 3)
        rand = random.randrange(1,4)
        
        if rand == 1:
            self.role = "마법사"
            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/01_magic.wav")
            pibo = cm.tts(bhv="do_explain_A", string="이제 우리는 하늘에 사는 마법사야. 파이보가 먼저 주문을 걸어볼게. 천둥아 쳐라 얍!")
            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/01_magic.wav")
            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/04_thunder.wav")
            
            pibo = cm.tts(bhv="do_suggestion_L", string=f"{wm.word(self.user_name, 0)}도 날씨 주문을 걸어봐! 먼저 비, 바람, 천둥 등 날씨를 말하고 얍!을 외치면 돼.")
            answer = cm.responses_proc(re_bhv="do_suggestion_L", re_q="날씨 주문을 걸어봐! 먼저 비, 바람, 천둥 등 날씨를 말하고 얍!을 외치면 돼.",
                                       neu_bhv="do_suggestion_S", neu="다른 주문을 걸어보자.",
                                       neg_bhv="do_suggestion_S", neg="다른 주문을 걸어보자.",
                                       feedback="N")
            
            if answer[0][0] == "action" or answer[0][0] == "positive":
                weather = ["비", "바람", "천둥", "눈", "해", "맑"]
                for i in range(len(weather)):
                    if weather[i] in answer[1]:
                
                        if "비" in answer[1]:   # "비바람" 도 여기 들어감
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/01_magic.wav")
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/02_rain.wav")
                            print("비")
                            
                        if "바람" in answer[1]:
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/01_magic.wav")
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/05_wind.wav")
                            print("바람")                            
                            
                        if "천둥" in answer[1]:
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/01_magic.wav")
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/04_thunder.wav")
                            print("천둥")                            
                        
                        if "눈" in answer[1]:
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/01_magic.wav")
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/06_snow.wav")  
                            print("눈")                                          
                        
                        if "해" or "맑" in answer[1]:
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/01_magic.wav")
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/03_clear.wav")    
                            print("해")
                        
                pibo = cm.tts(bhv="do_joy_A", string="우와. 주문을 잘 거는 걸?")    

            
            pibo = cm.tts(bhv="do_suggestion_S", string="이번에는 소풍가는 날에 원하는 날씨 주문을 걸어봐.")
            answer = cm.responses_proc(re_bhv="do_suggestion_S", re_q="소풍가는 날에 원하는 날씨 주문을 걸어봐.",
                                       neu_bhv="do_suggestion_S", neu="몰라도 괜찮아.", 
                                       feedback="N")
            
            if answer[0][0] == "action" or answer[0][0] == "positive": 
                weather = ["비", "바람", "천둥", "눈", "해", "맑"]
                for i in range(len(weather)):
                    if weather[i] in answer[1]:
                                        
                        if "비" in answer[1]:   # "비바람" 도 여기 들어감
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/01_magic.wav")
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/02_rain.wav")
                            print("비")
                            
                        if "바람" in answer[1]:
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/01_magic.wav")
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/05_wind.wav")
                            print("바람")                            
                            
                        if "천둥" in answer[1]:
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/01_magic.wav")
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/04_thunder.wav")
                            print("천둥")                            
                        
                        if "눈" in answer[1]:
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/01_magic.wav")
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/06_snow.wav")  
                            print("눈")                                          
                        
                        if "해" or "맑" in answer[1]:
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/01_magic.wav")
                            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/03_clear.wav")    
                            print("해")   
                        
                    pibo = cm.tts(bhv="do_joy_B", string="빨리 소풍 가고 싶다!")                
                
        if rand == 2:
            self.role = "도깨비"
            
            pibo = cm.tts(bhv="do_explain_A", string="이제 우리는 숲 속의 도깨비야. 파이보가 먼저 주문을 걸어볼게. 뻐꾸기야 나타나라 얍!")
            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/01_magic.wav")
            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/07_owl.wav")
            
            pibo = cm.tts(bhv="do_suggestion_L", string=f"{wm.word(self.user_name, 0)}도 마법 주문을 걸어서 동물을 불러봐! 동물 이름을 말하고 얍!을 외치면 돼.")
            
            pibo = cm.tts(bhv="do_suggestion_S", string=f"먼저 늑대를 불러보자!")
            answer = cm.responses_proc(re_bhv="do_suggestion_L", re_q="늑대를 불러보자!",
                                       neu_bhv="do_suggestion_S", neu="다른 주문을 걸어보자.",
                                       neg_bhv="do_suggestion_S", neg="다른 주문을 걸어보자.",
                                       feedback="N")
            
            if answer[0][0] == "action" or answer[0][0] == "positive":  
                if "늑대" in answer[1]:                    
                    audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/01_magic.wav")
                    audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/08_wolf.wav")
                    pibo = cm.tts(bhv="do_joy_A", string="늑대가 나타났다.")
                    
            pibo = cm.tts(bhv="do_suggestion_S", string="이번에는 코끼리를 불러보자!")
            answer = cm.responses_proc(re_bhv="do_suggestion_L", re_q="코끼리를 불러보자!",
                                       neu_bhv="do_suggestion_S", neu="몰라도 괜찮아.",
                                       feedback="N")

            if answer[0][0] == "action" or answer[0][0] == "positive":  
                if "코끼리" in answer[1]:                    
                    audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/01_magic.wav")
                    audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/09_elephant.wav")
                    pibo = cm.tts(bhv="do_joy_B", string="우와. 주문을 잘 거는 걸?")                
                
        if rand == 3:
            self.role = "요정"
            
            pibo = cm.tts(bhv="do_explain_A", string="이제 우리는 물에 사는 요정이야. 파이보가 먼저 주문을 걸어볼게. 바다 갈매기야 나타나라 얍!")
            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/01_magic.wav")
            audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/11_seagull.wav")
            
            pibo = cm.tts(bhv="do_suggestion_L", string=f"{wm.word(self.user_name, 0)}도 마법 주문을 걸어서 동물을 불러봐! 동물 이름을 말하고 얍!을 외치면 돼.")
            
            pibo = cm.tts(bhv="do_suggestion_S", string=f"물가에 사는 오리를 불러보자!")
            answer = cm.responses_proc(re_bhv="do_suggestion_L", re_q="오리를 불러보자!",
                                       neu_bhv="do_suggestion_S", neu="다른 주문을 걸어보자.",
                                       neg_bhv="do_suggestion_S", neg="다른 주문을 걸어보자.",
                                       feedback="N")
            
            if answer[0][0] == "action" or answer[0][0] == "positive":  
                if "오리" in answer[1]:                    
                    audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/01_magic.wav")
                    audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/12_duck.wav")
                    pibo = cm.tts(bhv="do_joy_A", string="귀여운 오리가 나타났다.")
                    
            pibo = cm.tts(bhv="do_suggestion_S", string="이번에는 개구리를 불러보자!")
            answer = cm.responses_proc(re_bhv="do_suggestion_L", re_q="코끼리를 불러보자!",
                                       neu_bhv="do_suggestion_S", neu="몰라도 괜찮아.",
                                       feedback="N")

            if answer[0][0] == "action" or answer[0][0] == "positive":  
                if "개구리" in answer[1]:                    
                    audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/01_magic.wav")
                    audio.audio_play("/home/pi/Pibo_Package_02/Pibo_Conversation/src/Roleplay/Sound/13_frog.wav")
                    pibo = cm.tts(bhv="do_joy_B", string="우와. 주문을 잘 거는 걸?")   
                    
        # 대화 시작
        pibo = cm.tts(bhv="do_explain_A", string=f"{wm.word(self.user_name, 0)}는 {wm.word(self.role, 1)} 되면 어떤 일을 하고 싶니?")
        answer = cm.responses_proc(re_bhv="do_explain_A", re_q=f"{wm.word(self.user_name, 0)}는 {wm.word(self.role, 1)} 되면 어떤 일을 하고 싶니?", 
                                   pos_bhv="do_question_S", pos=f"또 어떤 일을 하고 싶니?", 
                                   neu_bhv="do_compliment_S", neu=f"괜찮아. 생각이 나지 않을 수 있어", 
                                   act_bhv="do_question_S", act=f"또 어떤 일을 하고 싶니?")

        if answer[0][0] == "action" or answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"또 어떤 일을 하고 싶니?", 
                                       pos_bhv="do_joy_A", pos=f"소원이 이루어지면 정말 좋겠다.", 
                                       neu_bhv="do_compliment_S", neu=f"괜찮아. 생각이 나지 않을 수 있어.", 
                                       act_bhv="do_joy_A", act=f"소원이 이루어지면 정말 좋겠다.")

        pibo = cm.tts(bhv="do_explain_B", string=f"{wm.word(self.user_name, 0)}는 {wm.word(self.role, 1)} 되면 변신해보고 싶은 모습이 있니?")
        answer = cm.responses_proc(re_bhv="do_explain_B", re_q=f"{wm.word(self.user_name, 0)}는 {wm.word(self.role, 1)} 되면 변신해보고 싶은 모습이 있니?", 
                                   pos_bhv="do_question_S", pos=f"언제 변신하고 싶니?", 
                                   neu_bhv="do_compliment_S", neu=f"괜찮아. 바로 떠오르지 않을 수 있어.", 
                                   act_bhv="do_question_S", act=f"언제 변신하고 싶니?")
        
        if answer[0][0] == "action" or answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q="언제 변신하고 싶니?",
                                       pos_bhv="do_joy_A", pos="변신하면 멋지겠는걸?",
                                       neu_bhv="do_compliment_S", neu="괜찮아. 바로 떠오르지 않을 수 있어.",
                                       act_bhv="do_joy_A", act="변신하면 멋지겠는걸?")

        pibo = cm.tts(bhv="do_explain_C", string=f"{wm.word(self.role, 2)} 시간 마법 써서 가장 기뻤던 시간으로 갈 수 있어. {wm.word(self.user_name, 0)}는 다시 돌아가고 싶은 시간이 있니?")
        answer = cm.responses_proc(re_bhv="do_explain_C", re_q=f"{wm.word(self.user_name, 0)}는 다시 돌아가고 싶은 시간이 있니?", 
                                   pos_bhv="do_question_S", pos=f"가서 무엇을 하고 싶니?", 
                                   neu_bhv="do_compliment_S", neu=f"괜찮아. 생각이 나지 않을 수 있어.", 
                                   act_bhv="do_question_S", act=f"가서 무엇을 하고 싶니?")
        
        if answer[0][0] == "action" or answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"가서 무엇을 하고 싶니?", 
                                       pos_bhv="do_joy_B", pos=f"파이보도 같이 가고 싶은 걸?", 
                                       neu_bhv="do_compliment_S", neu=f"괜찮아. 생각이 나지 않을 수 있어.", 
                                       act_bhv="do_joy_B", act=f"파이보도 같이 가고 싶은 걸?")
    

        pibo = cm.tts(bhv="do_explain_C", string=f"{wm.word(self.role, 2)} 어렵고 힘든 사람들을 도와줄 수 있는 능력이 있어. {wm.word(self.user_name, 0)}는 {wm.word(self.role, 1)} 되면 누구를 도와주고 싶니?")
        answer = cm.responses_proc(re_bhv="do_explain_C", re_q=f"{wm.word(self.role, 1)} 되면 누구를 도와주고 싶니?", 
                                   pos_bhv="do_question_S", pos=f"어떤 도움을 주고 싶니?",     # 이름 확인/언급 일단 패스
                                   neu_bhv="do_compliment_S", neu=f"몰라도 괜찮아.", 
                                   act_bhv="do_question_S", act=f"어떤 도움을 주고 싶니?")
        
        if answer[0][0] == "action" or answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"어떤 도움을 주고 싶니? ", 
                                       pos_bhv="do_joy_B", pos=f"도움을 주면 정말 좋겠다!", 
                                       neu_bhv="do_compliment_S", neu=f"몰라도 괜찮아.", 
                                       act_bhv="do_joy_B", act=f"도움을 주면 정말 좋겠다!")
            
        pibo = cm.tts(bhv="do_explain_C", string=f"{wm.word(self.role, 2)} 사람들의 기분을 즐겁게 만들어 줄 수 있어. {wm.word(self.user_name, 0)}는 {wm.word(self.role, 1)} 되면 누구를 즐겁게 만들어 주고 싶니?")
        answer = cm.responses_proc(re_bhv="do_explain_C", re_q=f"{wm.word(self.role, 1)} 되면 누구를 즐겁게 만들어 주고 싶니?", 
                                   pos_bhv="do_question_S", pos=f"어떻게 하면 즐거워질까?",     # 이름 확인/언급 일단 패스
                                   neu_bhv="do_compliment_S", neu=f"괜찮아. 바로 떠오르지 않을 수 있어.", 
                                   act_bhv="do_question_S", act=f"어떻게 하면 즐거워질까?")
        
        if answer[0][0] == "action" or answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"어떻게 하면 즐거워질까?", 
                                       pos_bhv="do_joy_B", pos=f"정말 좋아할 것 같아!", 
                                       neu_bhv="do_compliment_S", neu=f"괜찮아. 답하기 어려울 수 있어.", 
                                       act_bhv="do_joy_B", act=f"정말 좋아할 것 같아!")
            
        pibo = cm.tts(bhv="do_explain_C", string=f"{wm.word(self.role, 2)} 원하는 곳 어느 장소든 갈 수 있어. {wm.word(self.user_name, 0)}는 어디에 가보고 싶니?")
        answer = cm.responses_proc(re_bhv="do_explain_C", re_q=f"{wm.word(self.user_name, 0)}는 어디에 가보고 싶니?", 
                                   pos_bhv="do_question_S", pos=f"가서 무엇을 하고 싶니?",     # 이름 확인/언급 일단 패스
                                   neu_bhv="do_compliment_S", neu=f"괜찮아. 바로 떠오르지 않을 수 있어.", 
                                   act_bhv="do_question_S", act=f"가서 무엇을 하고 싶니?")
        
        if answer[0][0] == "action" or answer[0][0] == "positive":
            answer = cm.responses_proc(re_bhv="do_question_S", re_q=f"가서 무엇을 하고 싶니?", 
                                       pos_bhv="do_joy_B", pos=f"파이보도 같이 가고 싶은 걸?", 
                                       neu_bhv="do_compliment_S", neu=f"괜찮아. 떠오르지 않을 수 있어.", 
                                       act_bhv="do_joy_B", act=f"파이보도 같이 가고 싶은 걸?")

        # 4. 마무리 대화
        pibo = cm.tts(bhv="do_joy_A", string=f"{wm.word(self.user_name, 0)}가 원하는 행복한 일들이 모두 이루어졌으면 좋겠다! 다음에 또 재미있는 역할놀이 하자.")    

        

  
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
    rop.Magician()