import time
import json
import schedule_run
from datetime import datetime, timedelta


def job(type):
    if type == 1:
        print("자연, 우리의 미래...")
    
    elif type == 2:
        print("우리, 자연의 미래...")
    
        
# def job2():
#     print("우리, 자연의 미래...")
    
# start = input("시작시간:")# '08:00'
# plus = int(input("시간간격:"))#20

# start_time = datetime.strptime(start, "%H:%M")
# later = start_time + timedelta(minutes=(plus))


for i in range(1, 2):
    print(i)
#     later = start_time + timedelta(minutes=((plus)*i))
#     test = datetime.strftime(later, "%H:%M")
#     print(later)
#     print(test)
    schedule_run.every().day.at("17:51:10").do(job, i)
    # schedule.every(3).seconds.do(job, i)
    print("f")
    schedule_run.clear()
    
    
# schedule.every(5).seconds.do(job, 2)


while True:
    schedule_run.run_pending()
    time.sleep(1)