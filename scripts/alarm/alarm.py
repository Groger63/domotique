
import os
from time import sleep
import time
import RPi.GPIO as GPIO
import time
from threading import Thread, Event, Lock
import atexit


import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


ALARM_ACTIVE = True

MY_ADDRESS = 'quentin.chambefort@free.fr'
PASSWORD = '(197969roger)'

# doorSensor = 23
pirSensor = 18
hallLight = 2 
# roomLight = 1
lightDuration = 20 

my_mutex = Event()

def initSensors() :
	#do something
	GPIO.setmode(GPIO.BCM)
	# GPIO.setup(doorSensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(pirSensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def switchLight(number,state) :
    if ALARM_ACTIVE :
        number = 0

    if ALARM_ACTIVE and state=='On' :
        os.system("./yeelight-shell-scripts/yeelight-disco.sh " + str(0) )
    else :
        os.system("./yeelight-shell-scripts/yeelight-scene.sh " + str(number) + " " + state)

def checkPirSensor() :
	if GPIO.input(pirSensor):
		return True 
	return False

def exit() :
	myMainThread.stopThread = True
	myMainThread.join()
	GPIO.cleanup()

class sleeperThread(Thread):

	time = 0
	stopThread = False

	def resetTimer(self) :
		my_mutex.set()
		self.time = lightDuration

	def run(self) :
		while not self.stopThread :
			self.time = self.time - 1
			sleep(1)
			if self.time <= 0 :
				switchLight(hallLight,'Off')
				my_mutex.clear()
				my_mutex.wait()

class mainThread(Thread):

	mySleeperThread = sleeperThread()
	stopThread = False

	def run(self):
		initSensors()
		self.mySleeperThread.start() 
		while not self.stopThread :
			if checkPirSensor():
				sendmail('intrusion')
				switchLight(hallLight,'On')
				self.mySleeperThread.resetTimer()
			time.sleep(0.2)
		self.mySleeperThread.stopThread = True 
		self.mySleeperThread.resetTimer()
		self.mySleeperThread.join()


def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """
    
    names = []
    emails = []
    with open(filename, mode='r') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r') as template_file:

        template_file_content = template_file.read()
    return Template(template_file_content)

def sendmail(filename):
    if ALARM_ACTIVE :
        templateFile = filename + '.txt'
        names, emails = get_contacts('contacts.txt') # read contacts
        message_template = read_template(templateFile)
        #name = 'Roger'
        #email = 'quentin.chambefort@gmail.com'
        # set up the SMTP server
        s = smtplib.SMTP(host='smtp.free.fr', port=25)
        s.starttls()
        #s.login(MY_ADDRESS, PASSWORD)
        # For each contact, send the email:
        for name, email in zip(names, emails):
        
            msg = MIMEMultipart()       # create a message

            # add in the actual person name to the message template
            message = message_template.substitute(PERSON_NAME=name.title())
    
            # Prints out the message body for our sake
    
            # setup the parameters of the message
            msg['From']=MY_ADDRESS
            msg['To']=email
            msg['Subject']="Intrusion appartement"
            
            # add in the message body
            msg.attach(MIMEText(message, 'plain'))
            
            # send the message via the server set up earlier.
            s.send_message(msg)
            del msg
        
        # Terminate the SMTP session and close the connection
        s.quit()
    

atexit.register(exit)
sendmail('init')
myMainThread = mainThread()

myMainThread.start()
while  True:
	pass
	
myMainThread.join()
