import os, sys
import re
import time
import random
import socket
from threading import Thread
import subprocess

from konlpy.tag import Komoran

# sys.path.append('/home/kiro/workspace/Conversation_Scenarios/data')
sys.path.append('/home/pi/Pibo_Package_02/Pibo_Play/data')

import google
from speech_to_text import speech_to_text
from text_to_speech import text_to_speech, TextToSpeech

from openpibo.device import Device
from openpibo.oled import Oled
import behavior.behavior_list as behavior
import behavior.eye_list as eye

"""
STT 모듈이랑 답변 처리 모듈 통합하고 있는 파일
    * class Dictionary: 답변 성격(Pos/Neu/Neg), 숫자 후보들
    * class ConversationManage: STT 모듈 -> 답변 처리 및 다음 발화+행동
    * class Socket_tr: socket 통신 모듈
"""

# transmit
# 클라이언트가 보내고자 하는 서버의 IP와 PORT
server_ip = "192.168.13.215"
server_port = 3000
server_addr_port = (server_ip, server_port)
buffersize = 2048

# receive
# 서버가 보내고자 하는 클라이언트의 IP와 PORT
client1_ip = "192.168.14.20"
client1_port = 5000
client1_addr_port = (client1_ip, client1_port)
buffersize = 2048

# UDP로 열고 서버의 IP/PORT 연결
# udp_client1_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# udp_client1_socket.bind(client1_addr_port)
# udp_client1_socket.setblocking(False)   


class Dictionary():
    
    def __init__(self):
        self.Yes = ['yes', '네', '예', '응', '어', '있어', '좋아', '좋은', '좋다', '그래', '맞아', '알았어', '알겠어', '당연', '됐어']

        self.No = ['no', '아니', '안', '별로', '글쎄', '싫어', '싫', '못 하', '못 하겠어', '못해', '없었어', '없어', '없네', '다른', '없다',
                   '없는', '몰라', '모르', '몰라', '그만', '없음']

        self.Done = ['done', '완료', '됐어', '했어', '했는', '하고', '하자', '할래', '왔어', '렸어', '시작', '끝', '다 만들었어', '다 그렸어', '다 오렸어', '다 올렸어', '성공', '이겼', '이긴', '승리', '왔어']

        self.Again = ['again', '다시', '또', '같은', '한 번 더', '한번 더', '계속']
        
        self.Chance = ['Chance', '찬스', '점']

        self.Animal = ['치타', '타조', '돌고래', '사슴', '호랑이', '고양이', '강아지', '수달', '코끼리', '토끼', '사자', '표범', 
                       '기린', '앵무새', '새', '공룡', '곰', '원숭이', '달팽이', '개미', '닭', '돼지', '소', '고슴도치', '개', '물고기', '다람쥐']
        
        self.Fruit = ['사과', '딸기', '복숭아', '포도', '귤', '오렌지', '감', '파인애플', '자두', '청포도', '바나나', '망고', '수박',
                        '배','참외', '앵두']        
        
        self.Number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

        self.Number_word = ['영', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구', '십']
        
        


class ConversationManage():

    def __init__(self):
        self.timeout = 10
        self.none = "None"
        self.next = "next"
        self.touch_count = 0
        self.user_said = ''
        self.stt_input = ''
        self.response = ''
        self.answer = []
        self.feedback = ''   
        # self.udp_client1_socket = socket
        # self.from_msg = ''     
        self.ko = -1
        self.nb = -1
        
        
    def stt(self):
        """         
        * 정상적인 응답이 들어왔을 경우: response = speech_to_text()
        * 무응답으로 timeout 발생한 경우: response = "None"
        """
        try:
            self.response = speech_to_text(timeout=self.timeout)
            
        except google.api_core.exceptions.DeadlineExceeded as e:
            print(e)
            self.response = self.none
        
        # 가끔 발생하는 Google API ERROR --> ignore
        except google.api_core.exceptions.Unknown as e:
            # print(e)
            self.response = self.none
        
        except google.api_core.exceptions.InvalidArgument as e:
            print(e)
            self.response = self.none
            
        except ValueError as e:     # timeout 시간 넘으면 그냥 retry call 안 하고 중단시킴 (/usr/local/lib/python3.7/dist-packages/google/api_core)
            print(e)                # # if deline is not None~Sleep generator stopped yielding sleep values.
            self.response = self.none
            
        except Exception as e:
            print(e)
            self.response = self.none

        return self.response
    
    
    def tts(self, bhv='do_stop', voice='nhajun', string=''):
        """
        * behavior: TTS 와 함께할 동작 ex. 'do_joy'
        * string: 발화할 TTS 내용
        """
        t = Thread(target=behavior.execute, args=([bhv]))
        t.start()
        
        while True:
            text_to_speech(voice=voice, text=string)
            break
        # t = Thread(target=text_to_speech, args=(voice, string))
        # t.start()
        
        # while True:
        #     time.sleep(1)
        #     behavior.execute(bhv)
        #     break    
        
        return string
        
    def responses_proc(self, re_bhv='', re_q=''):
        """
        * re_q: 무응답인 경우, 재질문할 내용(최대 3번)
        * pos/neu/neg: 긍정/중립/부정 답변 인식 시, 발화할 내용
        * 사용자가 발화한 내용 중 Dictionary에 포함되는 단어 있으면 return answer
            => Positive/Neutral/Negative
        * feedback: 옵션 답변 유무 결정(기본: Y)
        """                
        self.answer = []    # 마지막 answer가 'action'일 경우 초기화 안 되는 것 같아서  
        count = 0
        while True:
            audio.audio_play("/home/pi/trigger.wav", 'local', '-1800', False)
            # o.set_font(size=25)
            # o.draw_text((15,20), "듣는 중..."); o.show()
            o.draw_image("/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/icon/icon_recognition1.png"); o.show()    
            print("\n")                        
            
            t = Thread(target=eye.e_listen, args=(), daemon=True)
            t.start()
            while True:
                self.stt_input = cm.stt()
                break
            
            self.response = self.stt_input[0]
            self.touch_count = self.stt_input[1]
            
            # # 터치 오인식으로 음성인식 안 되고 넘어가는 경우 있는 것 같음. => 임시로 삭제함 (230718)
            # if self.touch_count == 2:     # touch 2번 => 다음 단계로 스킵
            #     # cm.tts(bhv="re_bhv", string="다음 단계로 넘어갈께~")  
            #     self.answer = self.next
            #     break
                        
            if self.stt_input != self.none:
                self.user_said = self.response
                break
            
            else:   # 무응답인 경우, 두 번 더 물어봐주고 3번째에도 무응답이면 탈출
                count += 1
                cm.tts(bhv=re_bhv, string=re_q)
                
                if count < 2:
                    continue 
                
                elif count == 2:
                    cm.tts(bhv="re_bhv", string="다음 단계로 넘어갈께~")
                    self.answer = self.next
                    break        
        
        """
        사용자가 발화한 내용에 포함되는 단어가 있다면 return answer '_'
        ex. input: 좋은 것 같아 ==> Yes=[..'좋은'..] ==> answer: Positive
        """
        
        for i in range(len(dic.Yes)):
            if dic.Yes[i] in self.user_said:     
                self.answer = ["yes", self.user_said]

        for j in range(len(dic.No)):
            if dic.No[j] in self.user_said:
                self.answer = ["no", self.user_said]
                
        for k in range(len(dic.Done)):
            if dic.Done[k] in self.user_said:
                self.answer = ["done", self.user_said]
        
        for m in range(len(dic.Again)):
            if dic.Again[m] in self.user_said:     
                self.answer = ["again", self.user_said]

        for n in range(len(dic.Chance)):
            if dic.Chance[n] in self.user_said:
                self.answer = ["chance", self.user_said]
                
        if len(self.answer) == 0:
            self.answer = ["action", self.user_said]    # pos -> neg -> neu 에도 없으면 act
            
        if self.answer == self.next:
            self.answer = ['next', 'Move on..']
        
        
        
        print("=>", self.answer)           
                
        # return self.answer
        return self.answer, count
    
    
class WordManage():
        
    def postposition(self, word):
        """
        'word' 가 종성으로 끝나는지 판별 (=받침이 있는지 없는지)
        """
        m = re.search("[가-힣]+", word)
        if m:
            k = m.group()[-1]
            return (ord(k) - ord("가")) % 28 > 0
        else:
            return
        
    
    def word(self, word, type):
        """
        type0: '다영'이 / '파이보'
        type1: '다영'이 / '파이보'가
        type2: '다영'은 / '파이보'는
        type3: '다영'을 / '파이보'를
        type4: '다영'아 / '파이보'야
        type5: '다영'과 / '파이보'와
        * 주의: 띄워쓰기 없어야 함 (ex. '작은 개구리' => '작은'의 영향 받는 듯;;)
        """
        if type == 0:
            name = f"{word}이" if wm.postposition(word) else f"{word}"
        if type == 1:
            name = f"{word}이" if wm.postposition(word) else f"{word}가"                    
        if type == 2:
            name = f"{word}은" if wm.postposition(word) else f"{word}는"              
        if type == 3:
            name = f"{word}을" if wm.postposition(word) else f"{word}를"
        if type == 4:
            name = f"{word}아" if wm.postposition(word) else f"{word}야"
        if type == 5:
            name = f"{word}과" if wm.postposition(word) else f"{word}와"

        return name


class NLP():
    
    def number(self, user_said):
        number = -1
        ko = -1
        nb = -1
        for i, j in enumerate(dic.Number_word):
            x = user_said.find(j)
            if x != -1:
                ko = i
        for i, j in enumerate(dic.Number):
            x = user_said.find(j)
            if x != -1:
                nb = i
        number = max(ko, nb)
        self.answer = number
        
        return self.answer
    
    
    def animal(self, user_said):
        """
        공백, 가, 을, 를 split 해서 리스트화
        ex. input: 나는 호랑이가 좋아! ==> animal: 호랑이   ... 나중에 수정하기
        => 이 부분에 komoran noun 적용하면 될 거 같음 (추후 수정!)
        """
        a_list = re.split('[ 가을를]', user_said)  

        animal = [i for i in a_list if i in dic.Animal]
        
        if len(animal) == 0:
            self.answer = user_said
        if len(animal) != 0:
            self.answer = animal[0]
            
        return self.answer
    
    
    def fruit(self, user_said):
        a_list = re.split('[ 가을를]', user_said)
        fruit = [i for i in a_list if i in dic.Fruit]
        
        if len(fruit) == 0:
            self.answer = user_said
        if len(fruit) != 0:
            self.answer = fruit[0]
            
        return self.answer
    
    def nlp_nouns(self, user_said):
        self.answer = kom.nouns(user_said)
        
        return self.answer
    
    
kom = Komoran()
dic = Dictionary()
cm = ConversationManage()
wm = WordManage()
nlp = NLP()
audio = TextToSpeech()
o = Oled()
d = Device()


            

if __name__ == "__main__":
    print("qq")
    answer = cm.responses_proc(re_bhv="do_stop", re_q="re_q")
    print(answer[0][0])
    # cm.touch()
  
#     # cm.responses_proc()

#     th1 = Thread(target=speech_to_text, args=())
#     th2 = Thread(target=cm.bt, args=())
    
#     th1.start(); th2.start()
    