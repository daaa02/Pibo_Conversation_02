import os, sys
import time

from openpibo.device import Device
from openpibo.oled import Oled
from openpibo.motion import Motion

sys.path.append('/home/pi/Pibo_Conversation')

motion = Motion()
device = Device()
oled = Oled()

oled.set_font(size=15)

oled.clear()
oled.draw_text((5,25), "업데이트 중입니다."); oled.show()

while True:
    os.system("sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get autoremove")
    # os.system("pip3 install --upgrade numpy") # 한 번 했으니까 안 해도 될 듯
    break

oled.clear()
oled.draw_text((15,25), "업데이트 완료!"); oled.show()

motion.set_motion("m_wakeup", 1)

os.system("python3 /home/pi/Pibo_Conversation/src/start_touch.py")