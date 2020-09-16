#import subprocess
import os
from picamera import PiCamera
from time import sleep
import smtplib
import time
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import RPi.GPIO as GPIO
import time

toaddr = 'quentin.chambefort@gmail.com'
me = 'Roger'
Subject='security alert'

GPIO.setmode(GPIO.BCM)

P=PiCamera()
P.resolution= (1024,768)
P.start_preview()
    
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
while True:
    if not GPIO.input(23):
        time.sleep(1)
	#subprocess.call(['./yeelight-shell-scripts/yeelight-toggle.sh 0'])
#	os.system('./yeelight-shell-scripts/yeelight-toggle.sh 0')
        print("Motion...")
	while not GPIO.input(23):
		time.sleep(1)
        #camera warm-up time
        time.sleep(10)
        P.capture('movement.jpg')
        time.sleep(10)
        subject='Security allert!!'
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = toaddr
        fp= open('movement.jpg','rb')
	img = MIMEImage(fp.read())
	fp.close()
        msg.attach(img)
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(user = 'quentin.chambefort@gmail.com',password='197969roger')
	text = msg.as_string()
        server.sendmail(me, toaddr, text)
#	server.send_message(msg)
        server.quit()


