import time
import json
import greengrasssdk
from gps3 import gps3

MqttTopic_GPS = "DFAS/GPS"

client = greengrasssdk.client("iot-data")

def function_handler(event, context):
	return

print("DFAS - GPS Module Starting initialization")

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

for new_data in gps_socket:
	if new_data:
		data_stream.unpack(new_data)
		if data_stream.TPV['time'] != 'n/a':
			print("New data received from GPS")
			print('time : ', data_stream.TPV['time'])
			print('lat : ', data_stream.TPV['lat'])
			print('lon : ', data_stream.TPV['lon'])
			print('alt : ', data_stream.TPV['alt'])
			print('speed : ', data_stream.TPV['speed'])
			client.publish(topic=MqttTopic_GPS, queueFullPolicy="AllOrException", payload=
				json.dumps({'time': data_stream.TPV['time'], 'lat': data_stream.TPV['lat'], 'lon': data_stream.TPV['lon']}))
			time.sleep(60)
