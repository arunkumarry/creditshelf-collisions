from flask import Flask, render_template
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_googlemaps import GoogleMaps
import pdb

app = Flask(__name__, template_folder="main/templates")
CORS(app)
app.config['MONGO_DBNAME'] = 'collisions'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/collisions'
app.config['GOOGLEMAPS_KEY'] = "AIzaSyCRgrK1ZVEZniDMHdcxf2A8tAH-nWbufD0"
GoogleMaps(app)
mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def hello():
	return render_template('home.html')

from app.main.controllers.collision import collision as collision_module
from app.main.controllers.bike_stations import bike_station as bike_stations_module
from app.main.controllers.maps import map_mod as map_module
app.register_blueprint(collision_module)
app.register_blueprint(bike_stations_module)
app.register_blueprint(map_module)