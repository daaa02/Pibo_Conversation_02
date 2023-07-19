# -*- coding: utf-8 -*-

# 귀가 후 요일 대화 시나리오

from datetime import datetime
import requests
import json
import random
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from NLP import NLP, Dictionary
from text_to_speech import TextToSpeech
# from speech_to_text import speech_to_text

nlp = NLP()
Dic = Dictionary()
tts = TextToSpeech()


def text_to_speech(text):
    filename = "tts.wav"
    print("\n" + text + "\n")
    tts.tts_connection(text, filename)
    tts.play(filename, 'local', '-800', False)


class Daily():
    
    def fb(self, option):
        if option == "pos":     # 긍정 답변 옵션
            feedback_list = ["정말? ", "그래? ", "그렇구나. ", "그랬구나. "]
            feedback = random.choice(feedback_list)
            
        elif option == "neg":   # 부정 답변 옵션
            feedback_list = ["그래? ", "그렇구나. ", "그랬구나. "]
            feedback = random.choice(feedback_list)
            
        elif option == "neu":   # 중립 답변 옵션
            feedback_list = ["그래? ", "음."]
            feedback = random.choice(feedback_list)
            
        elif option == "act":   # 행동 답변 옵션
            feedback_list = ["정말? ", "그래? ", "그렇구나. ", "그랬구나. "]
            feedback = random.choice(feedback_list)

        return feedback
    
    
    def weather(self):     
        # OpenWheather API 사용
        api_key = "0c82929609843a12a69548c79280c567" 
        city = "Seoul"
        lang = "kr"
        
        api_call = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang={lang}"  # 특정 도시의 날씨
        # api_call = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&lang={lang}"   # 특정 동네(위도, 경도)의 날씨
        
        result = requests.get(api_call)
        data = json.loads(result.text)
        
        print(f"\nWhere & Weather : {data['name']}, {data['weather'][0]['main']}")
        weather = data["weather"][0]["main"]

        
        # 날씨 목록: Thunderstorm(뇌우), Drizzle(이슬비), Rain(비), Snow(눈), Atmosphere(안개, 황사 등), Clear(맑음), Clouds(구름)         
        
        if weather in ["Thunderstorm", "Drizzle", "Rain"]: 
            text_to_speech("오늘은 비가 와서 야외 활동을 하기 힘들었겠는걸?")
        elif weather == "Snow":
            text_to_speech("오늘은 눈이 왔는데 야외 활동을 했니?")
        elif weather == "Clear":
            text_to_speech("오늘은 날씨가 좋아서 야외 활동을 하기 좋았겠는걸?")
        else:   # Atmosphere, Clouds
            text_to_speech("오늘은 야외 활동을 했니?")
    
    # 월요일
    def Monday(self, name):
        
        def key_conversation(name):
            text_to_speech(f"\n유치원에 가는 게 안 좋구나. 왜 안 좋을까? 친구들이 {name}이랑 같이 안 노니?")
            user_said = input("입력: ")
            user_said = nlp.nlp_answer(user_said=user_said, dic=Dic)
            print("\n")
            
            if user_said == "negative":
                text_to_speech(day.fb(option="pos") + "정말 속상하겠다. 언제부터 그랬니?")
                user_said = input("입력: ")                
                print("\n")
                
                text_to_speech(day.fb(option="act") + f"{name}가 힘들었겠구나.. 엄마에게 이야기를 좀 해볼래? 도움이 필요할 수도 있어.")
                print("\n")
                
            elif user_said == "positive":
                text_to_speech(day.fb(option="neg") + "그럼 어떤 것 때문에 유치원에 가기 힘드니?")
                user_said = input("입력: ")
                print("\n")
                
                text_to_speech(day.fb(option="act") + f"{name}가 힘들었겠구나.. 엄마에게 이야기를 좀 해볼래? 도움이 필요할 수도 있어.")
                print("\n")
                
            else:
                text_to_speech(day.fb(option="neu"))
                print("\n")
            
            text_to_speech("속상한 일이 있으면 언제든 나에게 이야기해도 좋아!\n")        
            # 끝
            
        text_to_speech(f"\n안녕 {name}아, 오늘 유치원 잘 다녀왔니?")
        user_said = input("입력: ")
        print("\n")
        
        text_to_speech(f"{name}아, 주말이 지나고 친구들이랑 만나서 재미있었겠다!")
        text_to_speech(f"오늘은 어떤 놀이를 했니?")
        user_said = input("입력: ")
        print("\n")
        
        text_to_speech(day.fb(option="act") + f"누구랑 함께 놀았니?")
        user_said = input("입력: ")
        print("\n")
        
        text_to_speech(day.fb(option="act") + f"{name}이는 좋아하는 놀이가 있니?")  # 기존: ㅇㅇ이는 무슨 놀이를 좋아하니?
        user_said = input("입력: ")
        user_said = nlp.nlp_answer(user_said=user_said, dic=Dic)
        print("\n")
        
        if user_said == "positive":
            text_to_speech(day.fb(option="pos") + "그 놀이할 때 어떤 게 가장 재미있니?")
            user_said = input("입력: ")
            print("\n")                        

            text_to_speech(day.fb(option="pos") + "그 놀이할 땐 어떤 장난감이 필요하니?")
            user_said = input("입력: ")
            print("\n")
            
            text_to_speech(day.fb(option="pos"))            
            print("\n")
                
        elif user_said == "negative":
            text_to_speech(day.fb(option="neg"))            
            print("\n")
            
        else: 
            text_to_speech(day.fb(option="neu"))
            print("\n")
        
        text_to_speech(f"내일도 유치원에 가지? {name}이는 유치원에 가는 게 좋니?")
        user_said = input("입력: ")
        user_said = nlp.nlp_answer(user_said=user_said, dic=Dic)
        print("\n")
        
        if user_said == "positive":
            text_to_speech(day.fb(option="pos") + "정말 유치원 생활이 재밌나 보구나!")
            print("\n")
            
        elif user_said == "negative":
            text_to_speech(day.fb(option="neg"))
            key_conversation(name)
            
        else:
            text_to_speech(day.fb(option="neu"))
            print("\n")
        
        text_to_speech("\n내일 챙겨가야 하는 준비물이 있니?")    # 기존: .준비물이 없니?
        user_said = input("입력: ")
        user_said = nlp.nlp_answer(user_said=user_said, dic=Dic)
        print("\n")
        
        if user_said == "positive":
           text_to_speech(day.fb(option="pos") + "부모님께 말씀드려서 잊지 않고 준비해가자!")
           print("\n")
           
        elif user_said == "negative":
            text_to_speech(day.fb(option="neg") + "내일은 준비물이 없는 날이구나.")
            print("\n")
            
        else: 
            text_to_speech(day.fb(option="neu") + "잘 생각해봐! 기억나면 부모님께 꼭 말씀드려서 잊지 않고 준비해가자!")
            print("\n")
        
        text_to_speech(f"내일도 {name}이가 유치원에서 좋은 하루를 보냈으면 좋겠어")
        text_to_speech("파이보가 기다리고 있을게. 내일도 이야기 하자!\n")     
            
    # 화요일
    def Tuesday(self, name):
        
        def key_conversation(name):
            text_to_speech(f"\n{name}아, 유치원에 {name}를 괴롭히는 친구가 있니?")
            user_said = input("입력: ")
            user_said = nlp.nlp_answer(user_said=user_said, dic=Dic)
            print("\n")
            
            if user_said == "positive":
                text_to_speech(day.fb(option="pos") + f"{name}를 괴롭히는 친구가 있구나.. 속상하겠는걸? 무슨 일이 있었는지 자세히 말해줄 수 있니?")
                user_said = input("입력: ")
                print("\n")
                
                text_to_speech(day.fb(option="act") + "\n엄마에게 이야기를 좀 해 볼래? 도움이 필요할 수도 있어")
                print("\n")
                
            elif user_said == "negative":
                text_to_speech(day.fb(option="neg"))
                print("\n")
                      
            else:
                text_to_speech(day.fb(option="neu"))
                print("\n")
            
            text_to_speech("속상한 일이 있으면 언제든 나에게 이야기해도 좋아!")  
            print("\n")
            # 끝

        text_to_speech(f"\n안녕 {name}아, 오늘 유치원 잘 다녀왔니?")
        user_said = input("입력: ")
        print("\n")
        
        text_to_speech(f"나는 나가지 않고도 날씨를 확인할 수 있단다")
        day.weather()
        user_said = input("입력: ")
        print("\n")
        
        text_to_speech(day.fb(option="pos"))
        print("\n")
              
        text_to_speech(f"오늘 유치원에서 어떤 재밌는 일이 있었니?")
        user_said = input("입력: ")
        print("\n")
        
        text_to_speech(day.fb(option="pos") + "오늘 유치원에서 힘든 일이 있었니?")   # 기존: .힘든 일은 없었니?
        user_said = input("입력: ")
        user_said = nlp.nlp_answer(user_said=user_said, dic=Dic)
        print("\n")
        
        if user_said == "positive":
            text_to_speech(day.fb(option="pos") + "어떤 일이니?") 
            user_said = input("입력: ")
            key_conversation(name)
            
        elif user_said == "negative":
            text_to_speech(day.fb(option="neg"))
            print("\n")
            
        else:
            text_to_speech(day.fb(option="neu"))
            print("\n")
            
        text_to_speech(f"{name}이는 유치원에서 누구랑 제일 친하니?")
        user_said = input("입력: ")
        print("\n")
        
        text_to_speech(day.fb(option="act") + "그 친구랑 뭐 하고 놀 때가 가장 재밌니?")
        user_said = input("입력: ")
        print("\n")
        
        text_to_speech(day.fb(option="act"))
        print("\n")
        
        text_to_speech(f"내일도 유치원에 가서 친구들이랑 사이좋게 놀아. 파이보가 {name}를 기다리고 있을게!\n")
        
    # 수요일             
    def Wensday(self, name, place):
        
        def key_conversation(name):
            text_to_speech(f"\n{place}에서 친구가 {name}를 때린 적 있니?")
            user_said = input("입력: ")
            user_said = nlp.nlp_answer(user_said=user_said, dic=Dic)
            print("\n")
            
            if user_said == "positive":
                text_to_speech(day.fb(option="pos") + f"친구가 {name}이를 때렸구나.. 속상했겠는 걸? 무슨 일이 있었는지 자세히 말해줄 수 있니?")
                user_said = input("입력: ")
                print("\n")
                
                text_to_speech(day.fb(option="act") + f"그 친구가 너를 때릴 때 너는 어떻게 했니?")
                user_said = input("입력: ")
                print("\n")
                
                text_to_speech(day.fb(option="act") + f"엄마에게 이야기를 좀 해 보는 건 어떨까? 도움이 필요할 수도 있어.")
                print("\n")
                
            elif user_said == "negative":
                text_to_speech(day.fb(option="neg"))
                print("\n")
                
            else:
                text_to_speech(day.fb(option="neu"))         
                print("\n")
            
            text_to_speech(f"속상한 일이 있으면 언제든 나에게 이야기해도 좋아!")
            print("\n")
            # 끝
        
        text_to_speech(f"\n안녕 {name}아, 어제는 {place} 잘 다녀왔니?")
        user_said = input("입력: ")
        print("\n")
        
        text_to_speech(f"어제 {name}이가 {place}에서 어떤 걸 배웠는지 궁금한 걸?")
        user_said = input("입력: ")
        print("\n")
        
        text_to_speech(f"새로 배운 노래가 있으면 나에게 들려줄 수 있니?")
        user_said = input("입력: ")
        
        text_to_speech(day.fb(option="act"))
        print("\n")
        
        text_to_speech(f"어제 {name}이가 {place}에서 했던 행동들 중에 파이보에게 꼭 얘기해주고 싶은 일이 있니?")
        user_said = input("입력: ")
        user_said = nlp.nlp_answer(user_said=user_said, dic=Dic)
        print("\n")
        
        if user_said == "positive":
            text_to_speech(day.fb(option="pos") + "어떤 일이었어?")
            user_said = input("입력: ")
            print("\n")
            
            text_to_speech(day.fb(option="act"))
            print("\n")
            
        elif user_said == "negative":
            text_to_speech(day.fb(option="neg"))
            print("\n")
        
        else:
            text_to_speech(day.fb(option="neu"))
            print("\n")
        
        text_to_speech(f"다른 친구들이나 선생님께 말하기 힘든 일이 있니?")   # 기존: 힘든 일은 없었니?
        user_said = input("입력: ")
        user_said = nlp.nlp_answer(user_said=user_said, dic=Dic)
        print("\n")
        
        if user_said == "positive":
            text_to_speech(day.fb(option="pos") + "어떤 일이었어?")
            user_said = input("입력: ")            
            key_conversation(name)
            
        elif user_said == "negative":
            text_to_speech(day.fb(option="neg"))
            print("\n")
        
        else:
            text_to_speech(day.fb(option="neu"))
            print("\n")
        
        text_to_speech(f"파이보는 {name}이가 {place}에서 있었던 일이 궁금해!")
        text_to_speech("무슨 일이든지 이야기해도 좋아! 파이보가 다. 들어줄게")
        
    # 목요일
    def Thursday(self, name):
        
        text_to_speech(f"\n안녕 {name}아, 유치원 잘 다녀왔니?")
        user_said = input("입력: ")
        print("\n")
        
        text_to_speech(f"오늘 점심은 뭘 먹었니?")
        user_said = input("입력: ")
        print("\n")
        
        text_to_speech(day.fb(option="act") + f"{name}이는 유치원에서 어떤 음식이 나올 때 제일 좋니?")
        user_said = input("입력: ")
        print("\n")
        
        text_to_speech(day.fb(option="act") + f"{name}이가 유치원에서 먹기 힘들다고 생각하는 음식은 뭐니?")
        user_said = input("입력: ")
        print("\n")
        
        text_to_speech(day.fb(option="act") + f"{name}이는 유치원에서 어떤 간식을 제일 좋아하니?")
        user_said = input("입력: ")
        print("\n")
        
        text_to_speech(day.fb(option="act") + f"그 간식이 자주 나오면 좋겠다!")
        print("먹기 싫은 음식도 골고루 한번 먹어보는 것도 좋을 것 같아!\n")
             
    # 금요일
    def Friday(self, name):
        
        def key_conversation(name):
            text_to_speech(f"\n{name}아, 울고 싶었던 적이 있니?")
            user_said = input("입력: ")
            user_said = nlp.nlp_answer(user_said=user_said, dic=Dic)
            print("\n")
            
            if user_said == "positive":
                text_to_speech(day.fb(option="pos") + f"{name}가 울고 싶었구나.. 정말 속상했었나보네. 언제 울고 싶었는지 말해줄 수 있어?")
                user_said = input("입력: ") 
                print("\n")
                               
                text_to_speech(day.fb(option="act"))
                print("\n")
                
            elif user_said == "negative":
                text_to_speech(day.fb(option="neg"))
                print("\n")
                
            else:
                text_to_speech(day.fb(option="neu"))
                print("\n")
            
            text_to_speech("속상한 일이 있으면 언제든 나에게 이야기해도 좋아!")
            print("\n")
            # 끝
            
        text_to_speech(f"\n안녕 {name}아, 유치원 잘 다녀왔니?")
        user_said = input("입력: ")
        print("\n")
        
        text_to_speech(f"벌써 금요일이야! 오늘은 어떤 재밌는 일이 있었니?")
        user_said = input("입력: ")
        user_said = nlp.nlp_answer(user_said=user_said, dic=Dic)
        print("\n")
        
        if user_said == "positive":
            text_to_speech(day.fb(option="pos") + f"비슷한 재밌는 일이 뭐가 있을까?")
            user_said = input("입력: ")      
            print("\n")      
            
            print(day.fb(option="act") + "정말 재미있었겠다!")
            print("\n")
            
        elif user_said == "negative":
            text_to_speech(day.fb(option="neg"))
            print("\n")
        
        else:
            text_to_speech(day.fb(option="neu"))
            print("\n")
        
        text_to_speech(f"{name}이는 속상한 일 있어?")    # 기존: 속상한 일은 없니?
        user_said = input("입력: ")
        user_said = nlp.nlp_answer(user_said=user_said, dic=Dic)
        print("\n")
        
        if user_said == "positive":
            text_to_speech(day.fb(option="pos"))
            key_conversation(name)
        
        elif user_said == "negative":
            text_to_speech(day.fb(option="neg"))
            
        else:
            text_to_speech(day.fb(option="neu"))
            key_conversation(name)
            
        text_to_speech(f"이번 주말에 {name}이가 하고 싶은 일이 있니?")
        user_said = input("입력: ")
        user_said = nlp.nlp_answer(user_said=user_said, dic=Dic)
        print("\n")
        
        if user_said == "positive":
            text_to_speech(f"어떤 멋진 계획이 있니?")
            user_said = input("입력: ")
            print("\n")
            
            print(day.fb(option="pos"))
            print("\n")
            
        elif user_said == "negative":
            text_to_speech(day.fb(option="neg") + f"{name}가 부모님께 놀러 가자고 말해 보는 건 어때?")
            user_said = input("입력: ")
            print("\n")
            
        else:
            text_to_speech(day.fb(option="neu") + f"{name}가 부모님께 놀러 가자고 말해 보는 건 어때?")
            user_said = input("입력: ")
            print("\n")
            
        text_to_speech(f"멋진 주말을 보내고 다음주에 파이보에게도 말해줘!\n")       
    


if __name__ == "__main__":
    day = Daily()
    name = input("\n이름 입력: ")
    place = input("장소 입력: ")
    today = 2    # datetime.now().weekday()
        
    if today == 0:      print("\n.Monday");      day.Monday(name)
    elif today == 1:    print("\n.Tuesday");     day.Tuesday(name)
    elif today == 2:    print("\n.Wensday");     day.Wensday(name, place)
    elif today == 3:    print("\n.Thursday");    day.Thursday(name)
    elif today == 4:    print("\n.Friday");      day.Friday(name)
    else:               print("\nWEEKEND!!");
    