import sys
import requests
import json
import pdb

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
				if collision["number_of_cyclist_injured"] or collision["number_of_cyclist_killed"]:
					cycle_collisions.append({"collision_id": collision["collision_id"],
						"lat": collision["latitude"],
						"long": collision["longitude"],
						"injured": collision["number_of_cyclist_injured"],
						"killed": collision["number_of_cyclist_killed"]})
			except KeyError: continue
		
		return json.dumps(cycle_collisions)


collisions = CollisionData(sys.argv[1])
print(collisions.get_by_borough())


