import os
from flask import Flask, render_template
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_googlemaps import GoogleMaps
from dotenv import load_dotenv
import logging

app = Flask(__name__, template_folder="main/templates")
CORS(app)

logging.basicConfig(filename='app.log', level=logging.DEBUG, 
		format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
	)
logger = logging.getLogger(__name__)

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

app.config['MONGO_DBNAME'] = os.getenv('MONGODB_NAME')
app.config['MONGO_URI'] = os.getenv('MONGODB_URI')
app.config['GOOGLEMAPS_KEY'] = os.getenv('GOOGLEMAPS_API_KEY')
app.config['TEMPLATES_AUTO_RELOAD'] = True
GoogleMaps(app)
mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def hello():
	return render_template('home.html')

from app.main.controllers.collisions import collision as collision_module
from app.main.controllers.bike_stations import bike_station as bike_stations_module
from app.main.controllers.maps import map_mod as map_module
app.register_blueprint(collision_module)
app.register_blueprint(bike_stations_module)
app.register_blueprint(map_module)