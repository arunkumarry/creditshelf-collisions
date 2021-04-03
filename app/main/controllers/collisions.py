from flask import Blueprint, request, jsonify
from app import mongo, logger
import pdb

collision = Blueprint('collision', __name__)

@collision.route('/boroughs', methods=['GET'])
def get_all_boroughs():
  collisions = mongo.db.collisions
  output = []
  logger.info("Getting all the boroughs")
  for collision in collisions.find():
    try:
      if collision['borough'] not in output:
        output.append(collision['borough'])
    except KeyError:
      continue
  return jsonify({'result' : output})

@collision.route('/collisions', methods=['GET'])
def get_all_collisions():
  collisions = mongo.db.collisions
  output = []
  logger.info("Getting all the collisions")
  for collision in collisions.find():
    try:
      output.append({'collision_id' : collision['collision_id'],
        'borough': collision['borough'],
        'cyclists_injured' : collision['cyclists_injured'],
        'cyclists_killed': collision['cyclists_killed'],
        'latitude': collision['latitude'],
        'longitude': collision['longitude'],
      })
    except KeyError: 
      logger.debug('Collision {} faced key error'.format(collision['collision_id']))
      continue
  return jsonify({'result' : output})

@collision.route('/collisions/<string:borough>', methods=['GET'])
def get_collisions_by_borough(borough):
  collisions = mongo.db.collisions.find({'borough' : borough})
  output = []
  logger.info("Getting all the collisions in the borough - {}".format(borough))
  for collision in collisions:
    try:
      output.append({'collision_id' : collision['collision_id'],
        'borough': collision['borough'],
        'cyclists_injured' : collision['cyclists_injured'],
        'cyclists_killed': collision['cyclists_killed'],
        'latitude': collision['latitude'],
        'longitude': collision['longitude'],
      })
    except KeyError:
      logger.debug('Collision {} faced key error'.format(collision['collision_id']))
      continue
  return jsonify({'result' : output})

@collision.route('/collision/<string:collision_id>', methods=['GET'])
def get_one_collision(collision_id):
  collisions = mongo.db.collisions
  logger.info("Getting the collisions with ID - {}".format(collision_id))
  collision = collisions.find_one({'collision_id' : collision_id})
  if collision:
    try:
      output = {'collision_id' : collision['collision_id'],
        'borough': collision['borough'],
        'cyclists_injured' : collision['cyclists_injured'],
        'cyclists_killed': collision['cyclists_killed'],
        'latitude': collision['latitude'],
        'longitude': collision['longitude'],
      }
    except KeyError: 
      logger.debug('Collision {} faced key error'.format(collision['collision_id']))
      raise
  else:
    output = "No such collision"
  return jsonify({'result' : output})

@collision.route('/collision', methods=['POST'])
def add_collision():
  collisions = mongo.db.collisions
  try:
    collision_id = request.json['collision_id']
    borough = request.json['borough']
    cyclists_injured = request.json['cyclists_injured']
    cyclists_killed = request.json['cyclists_killed']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
  except KeyError:
    output = "Post params are invalid"
    logger.error(output)
    raise

  logger.info("Creating collision with ID - {} if not present".format(collision_id))
  try:
    collision = collisions.update({'collision_id' : collision_id}, {'collision_id' : collision_id,
        'borough': borough,
        'cyclists_injured' : cyclists_injured,
        'cyclists_killed': cyclists_killed,
        'latitude': latitude,
        'longitude': longitude,
      }, upsert=True)
  except Exception as e:
    output = str(e)
    logger.error(output)
    raise
  
  new_collision = collisions.find_one({'_id': collision })
  logger.info("Collision created - {}".format(str(new_collision)))
  output = {'collision_id' : new_collision['collision_id'],
      'borough': new_collision['borough'],
      'cyclists_injured' : new_collision['cyclists_injured'],
      'cyclists_killed': new_collision['cyclists_killed'],
      'latitude': new_collision['latitude'],
      'longitude': new_collision['longitude'],
    }
  return jsonify({'result' : output})