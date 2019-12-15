from task1 import geocode
from time import sleep
input = open("bus_stand_names.txt",'r')
output = open("long_and_lat.txt", 'w')
data_lines = input.readlines()
count = 0

test = "Adur bus stand"

API_key = "AIzaSyCbGanFV33ibPvYaQwyxi9e4fEBoXwu_x0"
out = geocode(test, API_key)
print(test + " " + str(out['latitude']) + " " + str(out['longitude']))
"""
for data in data_lines:
	data = data[:len(data)-1]
	address = data + " bus stop, bangalore"
	API_key = "AIzaSyCbGanFV33ibPvYaQwyxi9e4fEBoXwu_x0"
	out = geocode(address, API_key)
	print(data + " " + str(out['latitude']) + " " + str(out['longitude']))
	output.write(data + " " + str(out['latitude']) + " " + str(out['longitude'])+"\n")
	sleep(0.04)	
"""