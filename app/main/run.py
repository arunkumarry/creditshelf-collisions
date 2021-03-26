# mongo.py

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'collisions'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/collisions'

mongo = PyMongo(app)

@app.route('/collisions', methods=['GET'])
def get_all_collision():
  collisions = mongo.db.collisions
  output = []
  for collision in collisions.find():
    output.append({'collision_id' : collision['collision_id'],
      'borough': collision['borough'],
      'cyclists_injured' : collision['cyclists_injured'],
      'cyclists_killed': collision['cyclists_killed'],
      'latitude': collision['latitude'],
      'longitude': collision['longitude'],
    })
  return jsonify({'result' : output})

@app.route('/collision/<string:collision_id>', methods=['GET'])
def get_one_collision(collision_id):
  collisions = mongo.db.collisions
  collision = collisions.find_one({'collision_id' : collision_id})
  if collision:
    output = {'collision_id' : collision['collision_id'],
      'borough': collision['borough'],
      'cyclists_injured' : collision['cyclists_injured'],
      'cyclists_killed': collision['cyclists_killed'],
      'latitude': collision['latitude'],
      'longitude': collision['longitude'],
    }
  else:
    output = "No such collision"
  return jsonify({'result' : output})

@app.route('/collision', methods=['POST'])
def add_collision():
  collisions = mongo.db.collisions
  collision_id = request.json['collision_id']
  borough = request.json['borough']
  cyclists_injured = request.json['cyclists_injured']
  cyclists_killed = request.json['cyclists_killed']
  latitude = request.json['latitude']
  longitude = request.json['longitude']
  collision = collisions.insert({'collision_id' : collision_id,
      'borough': borough,
      'cyclists_injured' : cyclists_injured,
      'cyclists_killed': cyclists_killed,
      'latitude': latitude,
      'longitude': longitude,
    })
  new_collision = collisions.find_one({'_id': collision })
  output = {'collision_id' : new_collision['collision_id'],
      'borough': new_collision['borough'],
      'cyclists_injured' : new_collision['cyclists_injured'],
      'cyclists_killed': new_collision['cyclists_killed'],
      'latitude': new_collision['latitude'],
      'longitude': new_collision['longitude'],
    }
  return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)
