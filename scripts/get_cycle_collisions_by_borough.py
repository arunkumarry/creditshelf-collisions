import sys
import requests
import json
import pdb

class CollisionData:
	def __init__(self, borough=""):
		self.borough = borough.upper()

	def get_by_borough(self):
		cycle_collisions = []
		total_record = 1766639
		for offset in range(0,total_record,50000):
			if self.borough:
				uri = "https://data.cityofnewyork.us/resource/h9gi-nx95.json?borough=" + self.borough +'&'+'$limit=50000&$offset='+str(offset)
			else:
				uri = "https://data.cityofnewyork.us/resource/h9gi-nx95.json?$limit=50000&$offset="+str(offset)
			response = requests.get(uri)
			collisions = response.json()
			try:
				collisions[49999]
			except IndexError: break
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

try:
	collisions = CollisionData(sys.argv[1])
except IndexError:
	collisions = CollisionData()
finally:	
	print(collisions.get_by_borough())


