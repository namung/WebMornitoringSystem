import os
import smtplib
import sqlite3
import datetime

from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

con=sqlite3.connect('./iddatabase.db')
curs=con.cursor()
for row in curs.execute('SELECT * FROM user ORDER BY id DESC LIMIT 1'):
    Email = row[1]

from_addr = formataddr(('2조', 'rkfaorl1480@gmail.com'))
to_addr = formataddr(('user', Email))
session = None


def logData():
    con=sqlite3.connect('../sensorsData.db')
    curs=con.cursor()
    now = datetime.datetime.now()
    
    for row in curs.execute('SELECT * FROM VACCINE ORDER BY EXPIRATION_DATE ASC'):
        Shelf_life = row[3]
        Shelf_life_datetype = datetime.datetime.strptime(Shelf_life,'%Y-%m-%d')
        if Shelf_life_datetype < now:
            pass
        else:
            break
    
    Shelf_life_res = str(Shelf_life_datetype).split(" ")[0]
    return Shelf_life_res


def getDaysBefore(target_day):
    dList = target_day.split("-")
    year = int(dList[0])
    month = int(dList[1])
    day = int(dList[2])
    
    target_day = datetime.datetime(year, month, day)
    now = datetime.datetime.now()
    
    datetime_target_day = (target_day - now).days
    
    return datetime_target_day


def Send_mail():
    try:
        # SMTP 세션 생성
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.set_debuglevel(True)
        
        # SMTP 계정 인증 설정회
        session.ehlo()
        session.starttls()
        session.login('rkfaorl1480@gmail.com', 'gaeq ocqv tfvr gqmx')
     
        # 메일 콘텐츠 설정
        message = MIMEMultipart("alternative")
        
        # 메일 송/수신 옵션 설정
        message.set_charset('utf-8')
        message['From'] = from_addr
        message['To'] = to_addr
        message['Subject'] = '설정한 온도값을 벗어났습니다.'
     
        # 메일 콘텐츠 - 내용
        body = '''
        <h2>설정한 온도값을 벗어났습니다..</h2>
        <h4>최대한 빠른 시간내에 확인하여 주십시오.</h4>
        <BODY>
        <IMG SRC="https://c.tenor.com/4qOJaZloJj4AAAAi/tag.gif">
        </BODY>
        '''
        bodyPart = MIMEText(body, 'html', 'utf-8')
        message.attach( bodyPart )
        
        # 메일 발송
        session.sendmail(from_addr, to_addr, message.as_string())            
     
        print( 'Successfully sent the mail!!!' )
    except Exception as e:
        print( e )
    finally:
        if session is not None:
            session.quit()

if __name__ == '__main__':
    Send_mail()

        
