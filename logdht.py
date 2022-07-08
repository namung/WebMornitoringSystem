#-*- coding:utf-8 -*-
import time
import schedule
import sqlite3
from w1thermsensor import W1ThermSensor
#import Adafruit_DHT
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import pandas as pd
from pandas import DataFrame as df
import csv
import os
from datetime import date

dbname='sensorsData.db'  #데이터베이스랑 연결
now=datetime.datetime.now()  #현재 시간
today=now.strftime("%Y-%m") #문서를 만들때 써먹기 위한 년도와 달을 뺴오기
sensor = W1ThermSensor()
#hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
# 온도를 얻기위한 함수
# def getDHTdata():            
    # DHT22Sensor= Adafruit_DHT.DHT22
    # DHTpin = 12
    # hum,temp = Adafruit_DHT.read_retry(DHT22Sensor,DHTpin)
    # if hum is not None and temp is not None:
        # hum = round(hum)
        # temp = round(temp, 1)
        # return temp, hum
        
def getDHTdata(): 
    temperature = sensor.get_temperature()
    print("The temperature is %s celsius" % temperature)
    tem = round(temperature, 1)
    
    return tem
    
# 데이터를 저장하기 위한 함수
def logData (temp):
    getDHTdata()
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO DHT_data values(datetime('now','localtime'), (?), (?))", (temp, temp))
    conn.commit()
    conn.close()
    
#문서를 저장하기 위한 함수
def cvscreate():
    xx=[] # 리스트를 만든 이유는 포문을 돌려서 리스트에 한줄씩 추가해주기 위해서
    yy=[]
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    for row in curs.execute("SELECT timestamp FROM DHT_data"):
        xx.append(row[0])
    for row in curs.execute("SELECT temp FROM DHT_data"):
        yy.append(row[0])

    df=pd.DataFrame(list(zip(xx,yy)),columns=('time','temp'))#데이터 프레임을 만들어 주기
    if not os.path.isdir(today): #위에서 선언한 년도와 달일 중첩되지않을때 만들어준다 
        os.makedirs(today)
    filename=datetime.datetime.now().strftime("%Y-%m-%d") #파일이름을  설장해주기
    df.to_csv(today+'/'+filename+'.cvs') # df=데이터프레임으로 csv파일을 만들고 파일경로 설정해주기 
    curs.execute("DELETE FROM DHT_data") # 다음날의 데이터를 위해서 초기화 시키는 예제
    conn.commit()
    conn.close()

def main():
    temp = getDHTdata()
    logData(temp)
       

schedule.every().minute.at(":00").do(main)
schedule.every().minute.at(":10").do(main)
schedule.every().minute.at(":20").do(main)
schedule.every().minute.at(":30").do(main)
schedule.every().minute.at(":40").do(main)
schedule.every().minute.at(":50").do(main)
schedule.every().day.at("14:51").do(cvscreate)


while True:
    schedule.run_pending()
    time.sleep(1)
