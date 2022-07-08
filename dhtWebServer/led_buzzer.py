# import Adafruit_DHT
from w1thermsensor import W1ThermSensor
import RPi.GPIO as GPIO
from time import sleep
import time
import sqlite3 as sql
import send_email

# Pin defining and board mode
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# sensor = Adafruit_DHT.DHT22
# DHTpin = 18
sensor = W1ThermSensor()
led = 14
buzzer= 15

GPIO.setup(led, GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)

def tem():
    # temperature = Adafruit_DHT.read_retry(sensor, DHTpin)
    temperature = sensor.get_temperature()
    print("The temperature is %s celsius" % temperature)
    tem = round(temperature, 1)
    
    return temperature

def get_temperature_setting_value():
    con=sql.connect('../sensorsData.db')
    curs=con.cursor()
    
    while True:
        for row in curs.execute('SELECT * FROM TEMP_R ORDER BY CREATED_AT DESC LIMIT 1'):
            now_max = row[2]
            now_min = row[3]
        con.close()
        return now_max, now_min
        
        time.sleep(1)

# This function checks the threshold temperature and lights up an led
try:
    while True:
        res = tem()
        now_max, now_min = get_temperature_setting_value()
        print("now temperature: ", res)
        print("now setting - max temperature: ", now_max)
        print("now setting - min temperature: ", now_min)
        
        if res < now_min or res > now_max:
            GPIO.output(led, 1)
            GPIO.output(buzzer, 1)
            send_email.Send_mail()   
        else:
            GPIO.output(led, 0)
            GPIO.output(buzzer,0)
         
        time.sleep(1)
        
except KeyboardInterrupt:
    GPIO.cleanup((led, buzzer))
        
