from flask import Blueprint, request, jsonify
from app import mongo
import pdb
import json

bike_station = Blueprint('bike_station', __name__)


@bike_station.route('/bike_stations', methods=['GET'])
def get_all_bike_stations():
  bike_stations = mongo.db.bike_stations
  output = []
  for bike_station in bike_stations.find():
    try:
      output.append({'station_id' : bike_station['station_id'],
          'name': bike_station['name'],
          'latitude': bike_station['latitude'],
          'longitude': bike_station['longitude'],
        })
    except KeyError: continue
  return jsonify({'result' : output})

@bike_station.route('/bike_station', methods=['POST'])
def add_bike_station():
  bike_stations = mongo.db.bike_stations
  station_id = request.json['station_id']
  name = request.json['name']
  latitude = request.json['latitude']
  longitude = request.json['longitude']
  try:
    bike_station = bike_stations.update({'station_id' : station_id}, {'station_id' : station_id,
        'name': name,
        'latitude': latitude,
        'longitude': longitude,
      }, upsert=True)
    output = 'Successful'
  except Exception as e:
    output = str(e)

  return jsonify({'result' : output})

