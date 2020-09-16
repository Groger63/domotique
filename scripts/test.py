#from picamera import PiCamera
from time import sleep
#import smtplib
import time
#from datetime import datetime
#from email.mime.image import MIMEImage
#from email.mime.multipart import MIMEMultipart
import RPi.GPIO as GPIO
import atexit
def clean() :
	GPIO.output(4, GPIO.LOW)
	GPIO.output(17, GPIO.LOW)
	GPIO.output(27, GPIO.LOW)
	GPIO.output(22, GPIO.LOW)
	GPIO.cleanup()

atexit.register(clean)
#import time

#toaddr = 'quentin.chambefort@gmail.com'
#me = 'Roger'
#Subject='security alert'

GPIO.setmode(GPIO.BCM)

#P=PiCamera()
#P.resolution= (1024,768)
#P.start_preview()
    
GPIO.setup(23, GPIO.IN)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

GPIO.output(4, GPIO.LOW)
GPIO.output(17, GPIO.LOW)
GPIO.output(27, GPIO.LOW)
GPIO.output(22, GPIO.LOW)

while True:
#   if GPIO.input(23):
        print("Motion...")
	GPIO.output(4, GPIO.input(23))
	GPIO.output(17,GPIO.input(23))
	GPIO.output(27,GPIO.input(23))
	GPIO.output(22,GPIO.input(23))
        #camera warm-up time
        time.sleep(0.5)
#        P.capture('movement.jpg')
#        time.sleep(10)
#        subject='Security allert!!'
#        msg = MIMEMultipart()
#        msg['Subject'] = subject
#        msg['From'] = me
#        msg['To'] = toaddr
        
#        fp= open('movement.jpg','rb')
#        img = MIMEImage(fp.read())
#        fp.close()
#        msg.attach(img)

#        server = smtplib.SMTP('smtp.gmail.com',587)
#        server.starttls()
#        server.login(user = 'quentin.chambefort@gmail.com',password='197969roger')
#	text = msg.as_string()
#        server.sendmail(me, toaddr, text)
#	server.send_message(msg)
#        server.quit()
