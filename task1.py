import os
import numpy as np
import requests
import requests
import logging
import time
import json
from random import sample

 
logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)

# create console handler

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)



def geocode(address, api_key):
    geo = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(address)
    #geocode_url="https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA"
    if api_key != None:

        geo = geo + "&key={}".format(api_key)

    res = requests.get(geo)

    # Results will be in JSON format - convert to dict using requests functionality

    json_data = json.loads(res.text)

    #print(json_data) #billing information is needed for this error is coming
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

def make_data( size , output_file_name):
    output = open(output_file_name, "w")
    input = open("busstops.txt",'r')
    make_string =""
    for string in input:
        make_string+=str(string)
    json_data = json.loads(make_string)
    data_list = json_data["features"]
    

    rand = sample(range(2000), size)
    for val in rand:
        i = data_list[val]
        output.write(str(i["geometry"]["coordinates"][1]) + " " +str(i["geometry"]["coordinates"][0])+ " \n")
        print(str(i["geometry"]["coordinates"][1]) + " " +str(i["geometry"]["coordinates"][0]))  



def make_distance_matrix (input_file_name, output_file_name):

    output = open(output_file_name, "w")
    input1 = open(input_file_name,'r')
    input1 = input.readlines()

    osrm_url = 'http://127.0.0.1:5000/table/v1/driving/'

    for i in input1:
        i = i.split()
        osrm_url += str(i[1]) +','+str(i[0])+';'
    osrm_url = osrm_url[:len(osrm_url)-1]
    osrm_url+= '?annotations=distance'
    distance_json = requests.get(osrm_url)
    distance_data = json.loads(distance_json.text)
    for data in distance_data['distances']:
        for values in data:
            output.write(str(values)+ " ")
        output.write("\n")

    input1.close()
    output.close()

#make_distance_matrix('test_data3.txt', 'distance_matrix_test_case3.txt')
#make_data(1500,'test_data3.txt')

def main(input_map, geocode_file, API_KEY):

    """
    input_map is a map of Bus_stop:Load
    """

    input1 = input_map
    #print(input1)

    f = open(geocode_file,'w')
    f.write("12.7972 77.4239 \n") #Bosch Bidadi office 

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
        <latitude> <longitude> <name> 
        """

        j = str(out['latitude']) + " " + str(out['longitude']) + " " + j + "\n"
        #print(j)

        f.write(j)

    f.close()

