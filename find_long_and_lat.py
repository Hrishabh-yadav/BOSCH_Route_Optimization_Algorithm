import requests 
from bs4 import BeautifulSoup 
import csv 
from time import sleep
import os

## opening file which contains list of bus stands
## list containing bus stands names
file1 = open('bus_stand_names.txt', 'r')
name_list =[]
for name in file1:
	name1  =name
	for i in range(0, len(name1)):
		if name1[i] == ' ':
			name1= name1[:i]+'+'+name[i+1:]
	name_list.append(name1[0:len(name1)-1])
file2 = open('bus_stand_long_and_lat.txt', 'w')
file3 = open('bus_stand_not_found.txt','w')
def find_distance_from_source(detination):
	URL = "https://www.google.com/search?client=ubuntu&channel=fs&ei=_0flXa2XCIXyrAHH8JiwCw&q="+bus_stand_name+"+longitude&oq="+bus_stand_name+"longitude&gs_l=psy-ab.3...2175.11724..12229...6.0..1.251.3210.0j9j7......0....1j2..gws-wiz.......33i160j0i67j0i7i30j0.SXtKav47mcQ&ved=0ahUKEwjtktPuvJfmAhUFOSsKHUc4BrYQ4dUDCAo&uact=5"
	r = requests.get(URL) 
	data_from_web  = BeautifulSoup(r.content, 'html5lib') 
	data_from_web = str(data_from_web)
	data_point = data_from_web.find('Latitude:')
	start_point = data_point
	while(data_from_web[start_point] != '>'):
	   start_point+=1
	end_point = start_point
	while(data_from_web[end_point] != '<'):
	   end_point+=1
	final_data =[]
	final_data.append(data_from_web[start_point+1:end_point])
	data_point = data_from_web.find('Longitude:')
	start_point = data_point
	while(data_from_web[start_point] != '>'):
	   start_point+=1
	end_point = start_point
	while(data_from_web[end_point] != '<'):
	   end_point+=1
	final_data.append(data_from_web[start_point+1:end_point])
	return final_data
for i in range(1, len(name_list)):
	try :
		bus_stand_name =name_list[i]
		final_data = find_distance_from_source( bus_stand_name )
		print('Writing: Distance from  '+ bus_stand_name +" is: "+final_data[0]+" "+ final_data[1] +"\n")
		file2.write(bus_stand_name+" "+final_data[0]+" "+ final_data[1]+"\n")
		sleep(1)
	except IndexError:
		sleep(1)
		print(name_list[i] + " Not found")
		file3.write(name_list[i]+"\n")
		sleep(1)

