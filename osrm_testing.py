import requests 
from bs4 import BeautifulSoup 
import csv 


URL = 'http://router.project-osrm.org/route/v1/driving/13.388860,52.517037;13.397634,52.529407;13.428555,52.523219?overview=false'

r = requests.get(URL) 
for i in r:
	print(i)