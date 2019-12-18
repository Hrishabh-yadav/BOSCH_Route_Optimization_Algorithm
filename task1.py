import os
import numpy as np
import requests
import requests
import logging
import time
import json
from random import sample
import geopy.distance
import time
 
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
    input = open(input_file_name,'r')
    input1 = input.readlines()

    osrm_url = 'http://127.0.0.1:5000/table/v1/driving/'

    for i in input1:
        i = i.split()
        osrm_url += str(i[1]) +','+str(i[0])+';'
    osrm_url = osrm_url[:len(osrm_url)-1]
    osrm_url+= '?annotations=distance'
    distance_json = requests.get(osrm_url)
    distance_data = json.loads(distance_json.text)
    dist_mat = []
    for data in distance_data['distances']:
        dist_m1 = []
        for values in data:
            dist_m1.append(int(values))
            output.write(str(values)+ " ")
        dist_mat.append(dist_m1)
        output.write("\n")

    input.close()
    output.close()
    return dist_mat

#make_distance_matrix('test_data5.txt', 'distance_matrix_test_case3.txt')
#make_data(1500,'test_data3.txt')

def main(input_file, not_found_file ,geocode_file, API_KEY, Nodes):

    """
    input_map is a map of Bus_stop:Load
    """
    input1 = open(input_file, 'r').readlines()
    f = open(geocode_file,'w')
    f2 = open(not_found_file,'w')
    f.write("12.7972 77.4239 \n") #Bosch Bidadi office 
    node_file = open(Nodes, 'w')
    node_file.write("Bosch Bidadi\n")
    for i in input1:
        i = i.split()
        i = i[2:]
        name =""
        for val in i:
            name+=val
        i = name
        name = name + ' bus stop, bangalore'
        
        out = geocode(name, API_KEY)
        majestic_geocode = (12.9778, 77.5728)
        geocodes = (float(out['latitude']), float(out['longitude']))
        time.sleep(0.05)
        if geopy.distance.vincenty(majestic_geocode, geocodes).km > 150:
            out = geocode(i, API_KEY)
            geocodes = (float(out['latitude'], float(out['longitude'])))
            if geopy.distance.vincenty(majestic_geocode, geocodes).km > 150:
                f2.write(i+"\n")
                continue
            time.sleep(0.05)
        
        """
        write in new file with format: 
        <latitude> <longitude> <name> 
        """

        node_file.write(i+"\n")
        j = str(out['latitude']) + " " + str(out['longitude']) + "\n"
        print(j)
        f.write(j)
        f.close()
        f2.close()
        node_file.close()
        
