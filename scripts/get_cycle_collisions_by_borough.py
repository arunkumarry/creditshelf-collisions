import sys
import requests
import json

class CollisionData:
	def __init__(self, borough):
		self.borough = borough

	def get_by_borough(self):
		uri = "https://data.cityofnewyork.us/resource/h9gi-nx95.json?borough=" + self.borough
		response = requests.get(uri)
		collisions = response.json()
		cycle_collisions = []
		for collision in collisions:
			try:
				if int(collision["number_of_cyclist_injured"]) > 0 or int(collision["number_of_cyclist_killed"]) > 0:
					collision_data = {"collision_id": collision["collision_id"],
						"latitude": collision["latitude"],
						"longitude": collision["longitude"],
						"cyclists_injured": collision["number_of_cyclist_injured"],
						"cyclists_killed": collision["number_of_cyclist_killed"],
						"borough": collision["borough"]}
				
					save_collision_uri = requests.post('http://localhost:5000/collision', json=collision_data)
					cycle_collisions.append(save_collision_uri.json())
			except KeyError: continue
		
		print(cycle_collisions)
		return json.dumps(cycle_collisions)


collisions = CollisionData(sys.argv[1])
print(collisions.get_by_borough())


