import RPi.GPIO as GPIO
from datetime import datetime
import time
import os
import json
import random
import greengrasssdk


pin_rgbled_red = 36
pin_rgbled_green = 38
pin_rgbled_blue = 40


MqttTopic_Wind = "DFAS/Wind"

client = greengrasssdk.client("iot-data")


def function_handler(event, context):
	return

print("DFAS - Wind Speed Module Starting initialization")



def GetWindSpeed():
	return result

def LightRgb(color):
	if color == 0:  #Red, wind strong
		GPIO.output(pin_rgbled_red, GPIO.LOW)
		GPIO.output(pin_rgbled_green, GPIO.HIGH)
		GPIO.output(pin_rgbled_blue, GPIO.HIGH)
	if color == 1:  #Green, normal
		GPIO.output(pin_rgbled_red, GPIO.HIGH)
		GPIO.output(pin_rgbled_green, GPIO.LOW)
		GPIO.output(pin_rgbled_blue, GPIO.HIGH)
	if color == 2:  #Blue
		GPIO.output(pin_rgbled_red, GPIO.HIGH)
		GPIO.output(pin_rgbled_green, GPIO.HIGH)
		GPIO.output(pin_rgbled_blue, GPIO.LOW)

GPIO.setmode(GPIO.BOARD)
for i in (pin_rgbled_red, pin_rgbled_green, pin_rgbled_blue):
	GPIO.setup(i, GPIO.OUT, initial=GPIO.HIGH)   # Set pins' mode is output

try:
	GPIO.setmode(GPIO.BOARD)
	for i in (pin_rgbled_red, pin_rgbled_green, pin_rgbled_blue):
		GPIO.setup(i, GPIO.OUT, initial=GPIO.HIGH)   # Set pins' mode is output

	while True:
		tmpWind = random.randint(0,54) / 10
		now = datetime.now()
		print("Current wind speed (using random) is : ", str(tmpWind))
		client.publish(topic=MqttTopic_Wind, queueFullPolicy="AllOrException", payload=
			json.dumps({'time': now.strftime("%m/%d/%Y, %H:%M:%S"), 'Wind': tmpWind}))
		if tmpWind > 5:
			LightRgb(0)
		else:
			LightRgb(1)
		
		time.sleep(5)

except Exception as e:
	print("Exception occured")
finally:
	GPIO.cleanup()



''' Using Webcame to capture real anemometer 
import pygame
import pygame.camera
import pygame.image
import boto3
client=boto3.client('rekognition', 
	region_name='ap-northeast-1',
	aws_access_key_id='AAA',
	aws_secret_access_key='BBB',
)

pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0")
cam.start()

for i in range(32):
	image= cam.get_image()


while True:
	image= cam.get_image()
	digit_area = pygame.Surface((200, 100))
	digit_area.blit(image, (0, 0), (100, 180, 200, 100))

	imgfile = 'tmp.jpg'
	pygame.image.save(digit_area, imgfile)
	
	with open(imgfile, 'rb') as image:
		response = client.detect_text(Image={'Bytes': image.read()})

	for label in response['TextDetections']:
		print (label['DetectedText'] + ' : ' + str(label['Confidence']))

	print("sleeping---------")
	time.sleep(5)
	
cam.stop()
'''