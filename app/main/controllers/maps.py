from flask import Blueprint, request, jsonify, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from app import mongo, logger
import pdb
import json
import reverse_geocoder as rg
from haversine import haversine, Unit
import os

map_mod = Blueprint('maps', __name__)

@map_mod.route('/map')
def mapview():
	collisions = mongo.db.collisions
	finlist = []
	# Get all the collisions
	logger.info("Get all the collisions and bike stations to dispaly on map")
	for coll in collisions.find():
		try:
			collision = {'lat': float(coll['latitude']),
				'lng': float(coll['longitude']),
				'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
				'infobox': "<b>Cyclists Injured: {}; Cyclists Killed: {}</b>".format(coll['cyclists_injured'], coll['cyclists_killed'])
			}
			logger.info("Added collision - {}".format(coll['collision_id']))
		except KeyError: continue
		finlist.append(collision)
	
	# Get all the bike stations
	bike_stations = mongo.db.bike_stations
	for bike_station in bike_stations.find():
		try:
			station = {'lat': float(bike_station['latitude']),
				'lng': float(bike_station['longitude']),
				'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
				'infobox': bike_station['name']
			}
			logger.info("Added bike station - {}".format(bike_station['name']))
		except KeyError: continue
		finlist.append(station)

	return render_template('map.html', raw_markers=json.dumps(finlist), googlemaps_key=os.getenv('GOOGLEMAPS_API_KEY'))

@map_mod.route('/map/collisions')
@map_mod.route('/map/collisions/<string:borough>', methods=['GET'])
def get_collision_locations_by_borough(borough="BRONX"):
	collisions = mongo.db.collisions
	finlist = []
	logger.info("Finding collisions in the borough - {}".format(borough))
	for coll in collisions.find({'borough' : borough}):
		try:
			collision = {'lat': float(coll['latitude']),
				'lng': float(coll['longitude']),
				'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
				'infobox': "<b>Cyclists Injured: {}; Cyclists Killed: {}</b>".format(coll['cyclists_injured'], coll['cyclists_killed'])
			}
		except KeyError: continue
		finlist.append(collision)

	return jsonify({'raw_markers': finlist})

@map_mod.route('/map/bike-stations', methods=['GET'])
def get_bike_stations():
	bike_stations = mongo.db.bike_stations
	finlist = []
	logger.info("Getting all bike stations")
	for bike_station in bike_stations.find():
		try:
			station = {'lat': float(bike_station['latitude']),
				'lng': float(bike_station['longitude']),
				'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
				'infobox': bike_station['name']
			}
			logger.info("Added bike station - {}".format(bike_station['name']))
		except KeyError: continue
		finlist.append(station)

	return jsonify({'raw_markers': finlist})


@map_mod.route('/map/bike-station-collisions', methods=['GET'])
def get_collisions_bike_stations():
	collisions = mongo.db.collisions
	try:
		position = request.args['position']
		station_name = request.args['station_id']
	except KeyError:
		logger.error('Request args are invalid')
		raise KeyError('Args are invalid')

	lat = float(position.split(',')[0])
	lng = float(position.split(',')[1])
	
	finlist = []
	# Find bike station by station_name
	logger.info("Finding stations in {}".format(station_name))
	try:
		station = mongo.db.bike_stations.find({'name': station_name})[0]
	except IndexError:
		logger.error('Station name {} not found'.format(station_name))
		raise IndexError('Station name not found')
	bike_station = {
		'lat': float(station['latitude']),
		'lng': float(station['longitude']),
		'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
		'infobox': station['name']
	}
	finlist.append(bike_station)

	logger.info("Finding collisions within 1 mile of the station location")
	for collision in collisions.find(): # Find collisions in borough from lat,lng
		try:
			dist = haversine((bike_station['lat'], bike_station['lng']), (float(collision['latitude']), float(collision['longitude'])), unit=Unit.MILES)
			rounded_dist = round(dist, 2)
			if rounded_dist < 1:
				collision_add = {'lat': float(collision['latitude']),
					'lng': float(collision['longitude']),
					'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
					'infobox': "<b>Cyclists Injured: {} <br>Cyclists Killed: {} <br>Distance to Station: {}miles</b>".format(collision['cyclists_injured'], collision['cyclists_killed'], rounded_dist)
				}
			else: continue
		except KeyError: continue
		except Exception as e:
			logger.error(str(e))
		finlist.append(collision_add)

	return jsonify({'raw_markers': finlist})