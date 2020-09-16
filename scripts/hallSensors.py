
import os
from time import sleep
import time
import RPi.GPIO as GPIO
import time


doorSensor = 23
pirSensor = 18
hallLight = 2
roomLight = 1
hallLightState = "Off"
lightDuration = 10 #seconds

def initSensors() :
	#do something
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(doorSensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(pirSensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	print("init done")

def checkDoorSensor() :
	if not GPIO.input(doorSensor):
		time.sleep(0.3)
		if not GPIO.input(doorSensor):
    			print("door oppened")
			return True 
	return False

def checkPirSensor() :
	if GPIO.input(pirSensor):
		print("pir detected")
		return True 
	return False

def switchLight(number,state) :
	global hallLightState
	if hallLightState == state :
		return
	print("switching state")
	os.system("./yeelight-shell-scripts/yeelight-scene.sh " + str(number) + " " + state  )
	hallLightState = state

def checkLoop() :
	if checkDoorSensor():
		if checkPirSensor(): #someone entered
			#do security stuff
			print("someone entered")
			switchLight(hallLight,'On')
			while checkDoorSensor() :
	        		time.sleep(1)
		else : #someone left
			print("someone left")
			while checkDoorSensor() :
				time.sleep(1)
			switchLight(hallLight,'Off')
	if checkPirSensor():
		print("motion detected")
		switchLight(hallLight,'On')
		while checkPirSensor() :
			time.sleep(lightDuration)
		switchLight(hallLight,'Off')

def main() :
	initSensors()
	while True :
		checkLoop()
		time.sleep(0.3)

main()
