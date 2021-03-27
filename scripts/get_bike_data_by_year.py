import boto3
import botocore
from botocore import UNSIGNED
from botocore.config import Config
import requests

BUCKET_NAME = 'tripdata' 
PATH = 'index.html' 

s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))

try:
    s3.Bucket(BUCKET_NAME).download_file(PATH, '201901-citibike-tripdata.csv.zip')
except botocore.exceptions.ClientError as e: 
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise
