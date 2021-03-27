from flask import Flask, render_template
from flask_cors import CORS
from flask_pymongo import PyMongo

app = Flask(__name__)
CORS(app)
app.config['MONGO_DBNAME'] = 'collisions'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/collisions'
mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def hello():
	return "Hello World"


from app.main.controllers.collision import collision as collision_module
app.register_blueprint(collision_module)