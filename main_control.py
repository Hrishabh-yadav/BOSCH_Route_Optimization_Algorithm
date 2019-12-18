import Algo_new
import takeInput
import task1
import time
import random
from sklearn.cluster import DBSCAN
start_time = time.time()




def testing():

	Algo_new.main('distance_matrix_test_case4.txt', 2000, 70)
	print("--- %s seconds ---" % (time.time() - start_time))

def testing2():
	task1.main('input.txt', 'not_found.txt','geocodes1.txt','AIzaSyCbGanFV33ibPvYaQwyxi9e4fEBoXwu_x0')

#testing2()

if __name__ == '__main__':

	# Basic Data
	geocode_file = 'long_lat.txt'
	geocode_file_new = 'lat_long.txt' #file containing lines of : <lat> <long> <bus_stop_name>
	distance_matrix_file = 'dist_mat.txt'
	demands_file = 'demands.txt' #lines of demands, zeroth demand = 0 for Bosch Bidadi office
	refined_input_file = 'refined_input.txt'#file containing lines of Bus_stop_name:load
	GEOCODE_API_KEY='AIzaSyCbGanFV33ibPvYaQwyxi9e4fEBoXwu_x0'
	not_found_file = "Not_Found.txt"
	node_names = "All_stop.txt"
	node_names_1 = "All_stop_1.txt"
	cluster_file = "Cluster.txt"
	ifile = "input.txt"
	operational_cost = 2000
	price_km = 13
	# Take initial input
	#ifile = input("Enter input file name: ") #which consists of lines of: <S_no> <Person_id> <Bus_stop_name>
	# max_bus = int(input("Enter maximum number of buses possible: ")) 

	# refine input, find demands
	
	# Compute geocode
	# writes <lat> <long> <bus_stop_name> to file passed as second argument
	# Also, he first entry in the geocode_file will be of BOSCH Bidadi office
	#task1.main(ifile, not_found_file, geocode_file, GEOCODE_API_KEY, node_names) 

	# Compute distance Matrix
	# zeroth place is Bosch Bidadi Office
	
	geocodes = open(geocode_file, 'r').readlines()
	new_geocode = open(geocode_file_new, 'w')
	nodes = open(node_names,'r').readlines()
	new_node_name = open(node_names_1, 'w')
	clust = open(cluster_file, 'w')
	demand = open(demands_file,'w')
	
	dist_mat = task1.make_distance_matrix(geocode_file, distance_matrix_file)
	cluster = DBSCAN(eps = 500, min_samples = 1).fit(dist_mat)
	labels = cluster.labels_
	clust.write(str(labels))
	demand_list = []
	map1 = {}
	for i in range(0, len(labels)):
		if map1.get(labels[i]) == None  : 
			new_geocode.write(geocodes[labels[i]])
			new_node_name.write(nodes[labels[i]])
			map1[labels[i]] = 1
		else:
			map1[labels[i]] += 1
	for i in map1:
		if i  == 0:
			demand_list.append((i, 0))
		else:
			demand_list.append((i, map1[i]))
	demand_list.sort()
	for i in demand_list:
		demand.write(str(i[1])+"\n")
	demand.close()
	new_geocode.close()
	clust.close()
	new_node_name.close()
	dist_mat = task1.make_distance_matrix(geocode_file_new, distance_matrix_file)
	
	Algo_new.main(distance_matrix_file, demands_file, operational_cost, price_km)
