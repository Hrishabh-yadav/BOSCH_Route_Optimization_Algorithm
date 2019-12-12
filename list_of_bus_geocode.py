import json
input = open("busstops.txt",'r')
s =""
output = open("long_and_lat.txt",'w')
for i in input:
	s+=str(i)
var = json.loads(s)
list_data = var["features"]
for i in list_data:
	#print(i)
	output.write(i["properties"]["name"] + "  " + str(i["geometry"]["coordinates"][1]) + " " +str(i["geometry"]["coordinates"][0])+ " \n")
	print(i["properties"]["name"] + "  " + str(i["geometry"]["coordinates"][1]) + " " +str(i["geometry"]["coordinates"][0]))  