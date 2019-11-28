import requests 
from bs4 import BeautifulSoup 
import csv 
import os 
URL = "https://narasimhadatta.info/bmtc_query.html"
r = requests.get(URL) 
data_from_web  = BeautifulSoup(r.content, 'html5lib') 
options_from_web = data_from_web.find_all('option')
file_for_bus_names = open(os.getcwd() + '/bus_stand_names.txt','w') 
for names in options_from_web:
	names = str(names)
	names = names[8:len(names) - 9]
	if names == "Minimum Number of Hops":
		break
	file_for_bus_names.write(names + '\n')