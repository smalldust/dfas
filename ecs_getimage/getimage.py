from datetime import datetime, timezone
import tempfile
from flask import Flask, send_file
import boto3


ecs_access_key_id = "132192858434009865@ecstestdrive.emc.com"
ecs_secret_key = "Nuig0Cclfe/+RHZy0xm0xDGDde4fP/6X2jkZ/yC6"
ecs_endpoint_url = "https://object.ecstestdrive.com"
ecs_bucket_name = "dfasimage"


app = Flask(__name__)

@app.route("/getimage", methods=["GET"])
def GetImage():
	try:
		s3 = boto3.client(service_name='s3', aws_access_key_id=ecs_access_key_id, aws_secret_access_key=ecs_secret_key, endpoint_url=ecs_endpoint_url)

		file_list = s3.list_objects(Bucket = ecs_bucket_name)

		latest = datetime(1970, 1, 1, tzinfo=timezone.utc)

		for i in file_list["Contents"]:
			if i["LastModified"] > latest:
				latest = i["LastModified"]
				last_item = i

		tfile = tempfile.NamedTemporaryFile()

		s3.download_file(Bucket = ecs_bucket_name, Key = last_item["Key"], Filename = tfile.name)

		return send_file(tfile.name, attachment_filename='skycamera.jpeg', mimetype='image/jpg')
	finally:
		tfile.close()


if __name__ == "__main__":
	app.run(debug = False, host = "0.0.0.0", port=8060, threaded = True)