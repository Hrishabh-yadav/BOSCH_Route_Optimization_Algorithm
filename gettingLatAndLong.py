import time
import os

# download using --> $ pip3 install opencage
from opencage.geocoder import OpenCageGeocode

# generate your API KEY using GMail
key = 'Your API key as a string'

# create object
geocoder = OpenCageGeocode(key)

# load cities, appended with country name
appendingString = ' Bus Stand, India'

# get the bus stops here
path = os.getcwd() + '/busStops_1.txt'
busStops = open(path, 'r')

# path where you write lat and lng for that place
ll_path = os.getcwd() + '/latLong_1.txt'
ll_data = open(ll_path, 'w')


# >> Actual Writing here >>>>>>>>>>>>>>>>>
for busStop in busStops:
	# ~~~~~~~~~~~~~~~~~~ Real deal here: ~~~~~~~~~~~~~~~
	query = busStop.rstrip('\n') + appendingString
	results = geocoder.geocode(query)
	lat = results[0]['geometry']['lat']
	lng = results[0]['geometry']['lng']

	ll_data.write(str(lat) + ' ' + str(lng) + '\n')
	print('Done writing for ', busStop.rstrip('\n'),', with lat = ', lat, ' and lng = ', lng)
	time.sleep(1)
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

ll_data.close()
busStops.close()
print('Done')


# with open(path) as f:
# 	busStop = f.read()
# 	ll_data.write(busStop+appendingString)


# generate the latitudes and longitudes
# for query in queries:
# 	results = geocoder.geocode(query)
# 	print(results[0]['geometry']['lat'])
# 	print(results[0]['geometry']['lng'])



# >> Dry test >>>>>>>>>>

# sample = busStops.readline()
# query = sample.rstrip('\n') + appendingString
# results = geocoder.geocode(query)
# lat = results[0]['geometry']['lat']
# lng = results[0]['geometry']['lng']

# ll_data.write(str(lat) + ' ' + str(lng) + '\n')


# ll_data.close()
# busStops.close()
# print('Done')

# >>>>>>>>>>>>>>>>>>>>>>
# ll_data.write(busStop+appendingString)  --> this adds India to next line --> waste!
# ll_data.write(data+appendingString+'\n')   --> hreat! it worked

