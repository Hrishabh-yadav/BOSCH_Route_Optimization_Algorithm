import json
from random import sample
"""list_data = var["features"]
for i in list_data:
	output.write(i["properties"]["name"] + "  " + str(i["geometry"]["coordinates"][1]) + " " +str(i["geometry"]["coordinates"][0])+ " \n")
	print(i["properties"]["name"] + "  " + str(i["geometry"]["coordinates"][1]) + " " +str(i["geometry"]["coordinates"][0]))  
"""




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


make_data(500, "test_data1.txt")