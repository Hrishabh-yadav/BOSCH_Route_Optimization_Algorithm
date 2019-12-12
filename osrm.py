import requests
import json

file = open('bus_stand_long_lat.txt','r')
coordinates = []
for f in file:
	data = f.split(' ')
	#print(data)
	if data[1] == 'bus+stand':
		data[1] = data[2]
		data[2] = data[3]
		data[3] = data[4]
	##print(data)
	new_val = data[3][:len(data[3])-1]
	##print(new_val)
	coordinates.append((data[0],data[1],new_val))

url =  'http://127.0.0.1:5000/table/v1/driving/'+coordinates[0][2] + ','+coordinates[0][1]
for i in range(1,len(coordinates)):
	url += ';'+coordinates[i][2]+','+coordinates[i][1]
url+= '?annotations=distance'
print(url)
file = open('distance_matrix.txt', 'w')
r = requests.get(url)
json_data = json.loads(r.text)
print(json_data['distances'])

for data in json_data['distances']:
	for i in data:
		i = str(i)
		file.write(i+" ")
	file.write('\n')

