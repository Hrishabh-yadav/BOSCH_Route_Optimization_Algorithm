from Algo_ortool import main
from task1 import take_input, geocode, make_distance_matrix
import time
import random
start_time = time.time()




def testing():
	main('distance_matrix_test_case1.txt')
	print("--- %s seconds ---" % (time.time() - start_time))


testing()