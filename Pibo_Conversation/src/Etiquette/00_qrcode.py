# -*- coding: utf-8 -*-

# 사회기술-QR코드 인식

import os, sys
import time
import json

sys.path.append('/home/pi/Pibo_Conversation/')
from data.c_conversation_manage import ConversationManage, WordManage, NLP

from openpibo.vision import Camera
from openpibo.vision import Detect

cm = ConversationManage()
wm = WordManage()

camera = Camera()
detect = Detect()



class Etiquette():  
    
    def __init__(self): 
        self.card_msg = ''
        self.act = ''
        
    
    def Card(self):
        
        cm.tts(bhv="do_suggestion_L", string=f"예절 카드를 파이보에게 보여줘!")
        
        while True: 
            time.sleep(2)
            img = camera.read()
            qr = detect.detect_qr(img)
            self.card_msg = qr['data']
            
            if len(self.card_msg) != 0:
            
                if self.card_msg == "차례대로 순서를 지켜요":
                    self.act = '02_sequence'
                    break
                    
                if self.card_msg == "입을 가리고 기침을 해요":
                    self.act = '03_cough'
                    break
                    
                if self.card_msg == "길을 걸으면서 뛰거나 장난치지 않아요":
                    self.act = '06_street'
                    break                    
                
                if self.card_msg == "아무 곳에나 낙서를 하지 않아요":
                    self.act = '07_scribble'
                    break                
                                        
                if self.card_msg == "장난감이나 놀이 기구를 양보해요":
                    self.act = '14_giveaway'  
                    break
                    
            else:
                cm.tts(bhv="do_suggestion_L", string=f"카드를 인식하지 못했어. 예절 카드를 다시 보여줄래?")
                continue
            
        os.system(f'python3 /home/pi/Pibo_Conversation/src/Etiquette/{self.act}.py')
            
        
        
        
        
if __name__ == '__main__':
    
    etq = Etiquette()
    etq.Card()