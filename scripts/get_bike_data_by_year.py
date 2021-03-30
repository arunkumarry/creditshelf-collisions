import boto3
import botocore
from botocore import UNSIGNED
from botocore.config import Config
import requests
from urllib.request import urlopen
import pdb
import zipfile
from io import BytesIO
import os
import csv

BUCKET_NAME = 'tripdata'
PATH = 'index.html'

s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))


def get_all_files_by_year():
	try:
		bike_files = s3.Bucket(BUCKET_NAME).objects.all()
		for bike_file in bike_files:
			print(bike_file.key)
			if bike_file.key.startswith('2019'):
				filebytes = BytesIO(bike_file.get()['Body'].read())
				myzipfile = zipfile.ZipFile(filebytes)
				for zip_info in myzipfile.infolist():
					if zip_info.filename.startswith('2019'):
						print(zip_info.filename)
						myzipfile.extract(zip_info, '../resources')
					# zip_info.filename = os.path.basename(zip_info.filename)
	except botocore.exceptions.ClientError as e:
		if e.response['Error']['Code'] == "404":
			print("The object does not exist.")
		else:
			raise

def save_bike_stations_data():
	RESOURCES_PATH = "../resources"
	for file in os.listdir(RESOURCES_PATH):
		if file.startswith('2019'):
			csv_file = RESOURCES_PATH + '/' + str(file)
			with open(csv_file, 'r') as file:
				csv_file = csv.DictReader(file)
				for row in csv_file:
					bike_station = dict(row)
					start_station_data = {"station_id": bike_station['start station id'],
										"latitude": bike_station["start station latitude"],
										"longitude": bike_station["start station longitude"],
										"name": bike_station['start station name']}
					save_start_bike_station_uri = requests.post('http://localhost:5000/bike_station', json=start_station_data)
					print(save_start_bike_station_uri)
					end_station_data = {"station_id": bike_station['end station id'],
										"latitude": bike_station["end station latitude"],
										"longitude": bike_station["end station longitude"],
										"name": bike_station['end station name']}
					save_end_bike_station_uri = requests.post('http://localhost:5000/bike_station', json=end_station_data)
					print(save_end_bike_station_uri)

save_bike_stations_data()
