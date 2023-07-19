# -*- coding: utf-8 -*-

import io
import os
import requests
import json
import wave
import urllib.request
import time


def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class TextToSpeech():
    
    def tts_connection(self, voice, text, filename):
        # CLOVA auth-key
        client_id = "3qz5jqx2r0"
        client_secret = "zwB0Yb4UONPKaOKCjZkhsSl8REuKvJTYK2Esvr41"
        encText = urllib.parse.quote(text)
        data = f"speaker={voice}&volume=0&speed=1&pitch=0&format=wav&text=" + encText
        url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
        request.add_header("X-NCP-APIGW-API-KEY",client_secret)
        response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            with open(filename, 'wb') as f:
                f.write(response_body)
        else:
            print("Error Code:" + rescode)            
                

    # tts, 효과음 등 모든 오디오를 플레이하는 함수
    def audio_play(self, filename, out='local', volume='-1000', background=False):
        if not os.path.isfile(filename):
            raise Exception(f'"{filename}" does not exist')

        if not filename.split('.')[-1] in ['mp3', 'wav']:
            raise Exception(f'"{filename}" must be (mp3|wav)')

        if not out in ['local', 'hdmi', 'both']:
            raise Exception(f'"{out}" must be (local|hdmi|both)')

        if not isNumber(volume):
            raise Exception(f'"{volume}" is not Number')

        if type(background) != bool:
            raise Exception(f'"{background}" is not bool')

        opt = '&' if background else ''
        os.system(f'omxplayer -o {out} --vol {volume} {filename} {opt}')
        
        
    def stop(self):
        os.system('sudo pkill play')
        
        
tts = TextToSpeech()

def text_to_speech(voice='nhajun', text=''):
    filename = "/home/pi/tts.wav"
    print("\n" + text + "\n")
    tts.tts_connection(voice, text, filename)
    tts.audio_play(filename, 'local', '-800', False)
    time.sleep(0.5)


if __name__ == '__main__':
    text = "Hello World"
    text_to_speech(text=text)