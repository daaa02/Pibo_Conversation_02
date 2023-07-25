#!/usr/bin/python3
import sys
import time

sys.path.append('/home/pi/Pibo_Conversation/data/behavior/icon/')

# openpibo module
from openpibo.oled import Oled

o = Oled()

# draw_image 하고 바로 show 해야 안 사라짐

def run():
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_question1.png")
    o.show()


def o_question():
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_question1.png")
    o.show()


def o_suggestion():
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_question2.png")
    o.show(); time.sleep(1)
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_question3.png")
    o.show(); time.sleep(1)


def o_explain():
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_step1.png")
    o.show(); time.sleep(1)
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_step2.png")
    o.show(); time.sleep(1)
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_step3.png")
    o.show(); time.sleep(1)


def o_photo():
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_camera.png")
    o.show()


def o_stamp():
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_stamp1.png")
    o.show(); time.sleep(1)
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_stamp2.png")
    o.show(); time.sleep(1)
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_stamp3.png")
    o.show(); time.sleep(1)
    

def o_waiting():
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_waiting1.png")
    o.show(); time.sleep(2)
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_waiting2.png")
    o.show(); time.sleep(2)
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_waiting3.png")
    o.show(); time.sleep(2)


def o_cheer():
    o.draw_image("/home/pi/Pibo_conversation/data/behavior/icon/icon_note1.png")
    o.show(); time.sleep(1)
    o.draw_image("/home/pi/Pibo_conversation/data/behavior/icon/icon_note2.png")
    o.show(); time.sleep(1)
    o.draw_image("/home/pi/Pibo_conversation/data/behavior/icon/icon_note3.png")
    o.show(); time.sleep(1)


def o_compliment():
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_good1.png")
    o.show(); time.sleep(1)
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_good2.png")
    o.show(); time.sleep(1)


def o_concil():
    o.draw_image("/home/pi/Pibo_conversation/data/behavior/icon/icon_default2.png")
    o.show()


def o_search():
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_detection1.png")
    o.show(); time.sleep(1)
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_detection2.png")
    o.show(); time.sleep(1)
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_detection3.png")
    o.show(); time.sleep(1)


def o_sleep():
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_sleep2.png")
    o.show(); time.sleep(1)
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_sleep1.png")
    o.show(); time.sleep(1)


def o_wakeup():
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_weather.png")
    o.show()


def o_agree():
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_o.png")
    o.show()


def o_deny():
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_x.png")
    o.show()


def o_joy():
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_default1.png")
    o.show(); time.sleep(1)
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_default2.png")
    o.show(); time.sleep(1)


def o_angry():
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_default2.png")
    o.show()


def o_sad():
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_default2.png")
    o.show()


def o_tired():
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_battery2.png")
    o.show(); time.sleep(1)
    o.draw_image("/home/pi/Pibo_Conversation/data/behavior/icon/icon_battery1.png")
    o.show(); time.sleep(1)

def o_listen():
    o.draw_image("/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/icon/icon_recognition3.png")
    o.show(); time.sleep(1)
    o.draw_image("/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/icon/icon_recognition2.png")
    o.show(); time.sleep(1)
    o.draw_image("/home/pi/Pibo_Package_02/Pibo_Play/data/behavior/icon/icon_recognition1.png")
    o.show(); time.sleep(1)