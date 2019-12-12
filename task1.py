import os
import numpy as np
import requests
import requests
import logging
import time
import json


logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)

# create console handler

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

def take_input():

    """
    input file consists lines of:
    
    S_No person_name Boarding_point

    """
    
    file = open('input.txt', 'r')
    input_list = file.readlines()

    """
	Converting to a map of Bus_stop_name:No_of_people 

    """
    map1 = {}
    

    for i in input_list:

    	# Convert input to string: "<name> bus stop, Bangalore"
    	j = i.split()
    	#print(j)
    	j = j[2:]
    	#print(j)
    	j = " ".join(j)
    	j+= " bus stop, Bangalore" 

    	#print(j)

    	if j in map1:
    		map1[j]+= 1
    	else:
    		map1[j] = 1
    file.close()

    return map1

def geocode(address, api_key):
    geo = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(address)
    #geocode_url="https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA"
    if api_key != None:

        geo = geo + "&key={}".format(api_key)

    res = requests.get(geo)

    # Results will be in JSON format - convert to dict using requests functionality

    json_data = json.loads(res.text)

    print(json_data) #billing information is needed for this error is coming
    res = res.json() #converting to json
    # if there's no results or an error, return empty results.
    if len(res['results']) == 0:

        output = {

            "formatted_address" : None,

            "latitude": None,

            "longitude": None

        }

    else:    

        answer = res['results'][0]

        output = {

            "formatted_address" : answer.get('formatted_address'),

            "latitude": answer.get('geometry').get('location').get('lat'),

            "longitude": answer.get('geometry').get('location').get('lng')
        }
    # Append some other details:    

    output['input_string'] = address
    output['status'] = res.get('status')
    output['response'] = res
    return output


if __name__ == "__main__":

	input1 = take_input()
	#print(input1)

	API_KEY='AIzaSyCbGanFV33ibPvYaQwyxi9e4fEBoXwu_x0'

	f = open('lat_long.txt','w')
	for i in input1:
		
		out = geocode(i, API_KEY)

		#If you just wanna test nd not use up requests, comment the above one and uncomment the below thing:
		#out ={'latitude': 4.99, 'longitude': 5.88}

		j = i.split()
		j = j[:-3]
		j = "+".join(j)
		#print(j)

		"""
		write in new file with format: 
		<name> <latitude> <longitude> <no_of_people>
		"""
		j = j + " " + str(out['latitude']) + " " + str(out['longitude']) + " " + str(input1[i]) + "\n"
		#print(j)

		f.write(j)

	f.close()