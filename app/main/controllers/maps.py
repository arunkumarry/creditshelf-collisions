from flask import Blueprint, request, jsonify, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from app import mongo
import pdb
import json
import reverse_geocoder as rg
from haversine import haversine, Unit

map_mod = Blueprint('maps', __name__)

@map_mod.route('/map')
def mapview():
	collisions = mongo.db.collisions
	finlist = []
	for coll in collisions.find():
		collision = {'lat': float(coll['latitude']),
			'lng': float(coll['longitude']),
			'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
			'infobox': "<b>Cyclists Injured: {}; Cyclists Killed: {}</b>".format(coll['cyclists_injured'], coll['cyclists_killed'])
		}
		finlist.append(collision)
	sndmap  = Map(
			identifier="sndmap",
			lat=-37.10054,
			lng=144.6300,
			markers= finlist
	)
	bike_stations = mongo.db.bike_stations
	for bike_station in bike_stations.find():
		station = {'lat': float(bike_station['latitude']),
			'lng': float(bike_station['longitude']),
			'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
			'infobox': bike_station['name']
		}
		finlist.append(station)

	return render_template('map.html',sndmap=sndmap, raw_markers=json.dumps(finlist))

@map_mod.route('/map/collisions')
@map_mod.route('/map/collisions/<string:borough>', methods=['GET'])
def get_collision_locations_by_borough(borough="BRONX"):
	collisions = mongo.db.collisions
	finlist = []
	for coll in collisions.find({'borough' : borough}):
		collision = {'lat': float(coll['latitude']),
			'lng': float(coll['longitude']),
			'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
			'infobox': "<b>Cyclists Injured: {}; Cyclists Killed: {}</b>".format(coll['cyclists_injured'], coll['cyclists_killed'])
		}
		finlist.append(collision)

	return jsonify({'raw_markers': finlist})

@map_mod.route('/map/bike-stations', methods=['GET'])
def get_bike_stations():
	bike_stations = mongo.db.bike_stations
	finlist = []
	for bike_station in bike_stations.find():
		station = {'lat': float(bike_station['latitude']),
			'lng': float(bike_station['longitude']),
			'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
			'infobox': bike_station['name']
		}
		finlist.append(station)

	return jsonify({'raw_markers': finlist})


@map_mod.route('/map/bike-station-collisions', methods=['GET'])
def get_collisions_bike_stations():
	collisions = mongo.db.collisions
	position = request.args['position']
	station_name = request.args['station_id']
	lat = float(position.split(',')[0])
	lng = float(position.split(',')[1])
	location = rg.search((lat,lng))
	address = location[0]['name']
	borough = address.upper()
	finlist = []
	station = mongo.db.bike_stations.find({'name': station_name})[0]
	bike_station = {
		'lat': float(station['latitude']),
		'lng': float(station['longitude']),
		'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
		'infobox': station['name']
	}
	finlist.append(bike_station)

	for collision in collisions.find({'borough': borough}):
		dist = haversine((bike_station['lat'], bike_station['lng']), (float(collision['latitude']), float(collision['longitude'])), unit=Unit.MILES)
		rounded_dist = round(dist, 2)
		collision_add = {'lat': float(collision['latitude']),
			'lng': float(collision['longitude']),
			'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
			'infobox': "<b>Cyclists Injured: {} <br>Cyclists Killed: {} <br>Distance to Station: {}miles</b>".format(collision['cyclists_injured'], collision['cyclists_killed'], rounded_dist)
		}
		finlist.append(collision_add)

	return jsonify({'raw_markers': finlist})