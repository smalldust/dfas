from picamera import PiCamera
from datetime import datetime, timedelta
import os
import time
import boto3

def function_handler(event, context):
	return

print("DFAS - Skycamera Module Starting initialization")

image_width = 720
image_height = 480
tmp_file = "skycamera_tmp.jpg"
photo_interval = 10

camera = PiCamera()
camera.awb_mode = 'auto'

time.sleep(2)

ecs_endpoint_url = 'https://object.ecstestdrive.com'
ecs_access_key_id = os.environ['ecs_access_key_id']  
ecs_secret_key = os.environ['ecs_secret_key']
ecs_bucket_name = os.environ['ecs_bucket_name']

s3 = boto3.client(service_name='s3', aws_access_key_id=ecs_access_key_id, aws_secret_access_key=ecs_secret_key, endpoint_url=ecs_endpoint_url)
if s3.head_bucket(Bucket=ecs_bucket_name):
	policy_status = s3.put_bucket_lifecycle_configuration(
				Bucket=ecs_bucket_name,
				LifecycleConfiguration={
						'Rules': 
							[{
									'Expiration': {
										'Days': 1
									},
									'Filter': {
										'Prefix': ''
									},
									'Status': 'Enabled',
									"ID": "RemoveOldImages"
								}]})


def function_handler(event, context):
	return

def upload_photo(file):
	now = datetime.now()
	expires = now + timedelta(minutes=5)
	session = boto3.resource(service_name='s3', aws_access_key_id=ecs_access_key_id, aws_secret_access_key=ecs_secret_key, endpoint_url=ecs_endpoint_url)
	filename = "sky" + datetime.now().strftime('%Y%m%d%H%M%S%f') + ".jpg"
	session.Object(ecs_bucket_name, filename).put(Body=open(file, 'rb'), Expires=expires)
	os.remove(file)

while True:
	camera.capture(tmp_file)
	upload_photo(tmp_file)
	time.sleep(10)
