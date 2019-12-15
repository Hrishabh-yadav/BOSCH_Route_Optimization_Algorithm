import Algo_ortool 
import takeInput
import task1
import time
import random
start_time = time.time()




def testing():
	Algo_ortool.main('distance_matrix_test_case4.txt')
	print("--- %s seconds ---" % (time.time() - start_time))



#testing()
if __name__ == '__main__':

	# Basic Data
	geocode_file = 'lat_long.txt' #file containing lines of : <lat> <long> <bus_stop_name>
	distance_matrix_file = 'dist_mat.txt'
	demands_file = 'demands.txt' #lines of demands, zeroth demand = 0 for Bosch Bidadi office
	refined_input_file = 'refined_input.txt'#file containing lines of Bus_stop_name:load
	GEOCODE_API_KEY='AIzaSyCbGanFV33ibPvYaQwyxi9e4fEBoXwu_x0'

	# Take initial input
	ifile = input("Enter input file name: ") #which consists of lines of: <S_no> <Person_id> <Bus_stop_name>
	# max_bus = int(input("Enter maximum number of buses possible: ")) 

	# refine input, find demands
	countmap = takeInput.main(ifile, refined_input_file, demands_file) #map of bus_stop:load

	# Compute geocode
	# writes <lat> <long> <bus_stop_name> to file passed as second argument
	# Also, he first entry in the geocode_file will be of BOSCH Bidadi office
	task1.main(countmap, geocode_file, GEOCODE_API_KEY) 

	# Compute distance Matrix
	# zeroth place is Bosch Bidadi Office
	task1.make_distance_matrix(geocode_file, distance_matrix_file)

	# run the algo
	Algo_ortool.main(distance_matrix_file, demands_file)