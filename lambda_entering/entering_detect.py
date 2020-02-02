import time
import pygame;
import RPi.GPIO as GPIO
import greengrasssdk

from datetime import datetime

lastEnter = None
enteringNow = False
EnteringRange = 1 			# 1 meters range
StayingTolerance = 5  		# Max 5 seconds staying in range
MqttTopic_Entering = "DFAS/EnteringDetection/Entering"
MqttTopic_Leaving = "DFAS/EnteringDetection/Leaving"

pin_ultrasound_trigger = 16
pin_ultrasound_echo = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_ultrasound_trigger, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_ultrasound_echo, GPIO.IN)


client = greengrasssdk.client("iot-data")


def CheckDist():
    GPIO.output(pin_ultrasound_trigger, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(pin_ultrasound_trigger, GPIO.LOW)
    while not GPIO.input(pin_ultrasound_echo):
        pass
    t1 = time.time()
    while GPIO.input(pin_ultrasound_echo):
        pass
    t2 = time.time()
    return (t2-t1)*340/2

def init():
	if pygame.mixer.get_init() == None:
		pygame.mixer.init()
		pygame.mixer.music.load('drone-notice.mp3')

def PlayNotice():
	if pygame.mixer.music.get_busy():
		return
	pygame.mixer.music.play()

def function_handler(event, context):
    return


print("DFAS - Entering Detection Module Starting initialization")


init()
try:
	while True:
		time.sleep(1)
		dist = CheckDist()
		print("Detected distance: ", str(dist))
		if dist < EnteringRange:
			if lastEnter:
				currentTime = time.time()
				if currentTime - lastEnter > StayingTolerance:
					lastEnter = None
					enteringNow = True
					now = datetime.now()
					client.publish(topic=MqttTopic_Entering, queueFullPolicy="AllOrException", payload=now.strftime("%m/%d/%Y, %H:%M:%S"))
					PlayNotice()
			else:
				lastEnter = time.time()
		else:
			if enteringNow:
				enteringNow = False
				client.publish(topic=MqttTopic_Leaving, queueFullPolicy="AllOrException", payload=now.strftime("%m/%d/%Y, %H:%M:%S"))

		
except Exception as e:
	print("Exception occured")
finally:
	pygame.mixer.quit()
	GPIO.cleanup()