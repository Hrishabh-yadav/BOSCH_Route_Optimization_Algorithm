import requests
import os 
API_key = "AIzaSyCbGanFV33ibPvYaQwyxi9e4fEBoXwu_x0"
place = "Kundalahalli Gate bus stop, Bangalore"
place = place.replace(' ','+')
URL = "https://maps.googleapis.com/maps/api/geocode/json?address="+place+"&key="+API_key
r = requests.get(URL)
for i in r:
	print(i)