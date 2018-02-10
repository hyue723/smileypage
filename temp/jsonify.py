import json

d = {"1": "16.2807333 -16.53877326",
	 "2": "3.34559232 8.65413288",
	 "3": "8.49563241 -83.65041661"}

with open('locations.json', 'w') as fp:
	json.dump(d, fp)