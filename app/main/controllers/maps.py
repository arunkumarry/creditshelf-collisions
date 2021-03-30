from flask import Blueprint, request, jsonify, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from app import mongo
import pdb
import json

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
