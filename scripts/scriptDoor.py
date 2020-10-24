
import os
from time import sleep
import time
import RPi.GPIO as GPIO
import time
from threading import Thread, Event, Lock
import atexit
from datetime import datetime

# doorSensor = 23
pirSensor = 18
hallLight = 2 
# roomLight = 1
lightDuration = 20

#les heures d'arrt
sunriseHour = 9 
sunriseMinute = 0
sunsetHour = 18
sunsetMinute = 30

my_mutex = Event()

def initSensors() :
	#do something
	GPIO.setmode(GPIO.BCM)
	# GPIO.setup(doorSensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(pirSensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def switchLight(number,state) :
	os.system("./yeelight-shell-scripts/yeelight-scene.sh " + str(number) + " " + state)


def checkPirSensor() :
	if GPIO.input(pirSensor):
		return True 
	return False

def exit() :
	myMainThread.stopThread = True
	myMainThread.join()
	GPIO.cleanup()

def checkTime() :
    currentTime = datetime.now()
    if currentTime.hour < sunriseHour :
        return True
    if currentTime.hour == sunriseHour and currentTime.minute <= sunriseMinute :
        return True
    if currentTime.hour >= sunsetHour :
        if currentTime.minute >= sunsetMinute :
            return True
    return False

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
                                if checkTime() :
            				switchLight(hallLight,'On')
	        			self.mySleeperThread.resetTimer()
                                else :
                                    print("c'est pas l'heure !") 
			time.sleep(0.01)
		self.mySleeperThread.stopThread = True 
		self.mySleeperThread.resetTimer()
		self.mySleeperThread.join()


atexit.register(exit)

myMainThread = mainThread()

myMainThread.start()
#while  True:
#	pass
	
myMainThread.join()

