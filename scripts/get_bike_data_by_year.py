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
import sys

BUCKET_NAME = 'tripdata'
PATH = 'index.html'

s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))


class BikeData:
	def __init__(self, year="2019"):
		self.year = year

	def get_all_files_by_year(self):
		try:
			bike_files = s3.Bucket(BUCKET_NAME).objects.all()
			for bike_file in bike_files:
				print(bike_file.key)
				if bike_file.key.startswith(self.year):
					filebytes = BytesIO(bike_file.get()['Body'].read())
					myzipfile = zipfile.ZipFile(filebytes)
					for zip_info in myzipfile.infolist():
						if zip_info.filename.startswith(self.year):
							print(zip_info.filename)
							myzipfile.extract(zip_info, '../resources')
		except botocore.exceptions.ClientError as e:
			if e.response['Error']['Code'] == "404":
				print("The object does not exist.")
			else:
				raise

	def save_bike_stations_data(self):
		RESOURCES_PATH = "../resources"
		for file in os.listdir(RESOURCES_PATH):
			if file.startswith(self.year):
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


try:
	bike_stations = BikeData(sys.argv[1])
except IndexError:
	bike_stations = BikeData()
finally:
	bike_stations.get_all_files_by_year()
	bike_stations.save_bike_stations_data()