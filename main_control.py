from Algo_ortools import main
from task1 import take_input, geocode, make_distance_matrix
import time
import random
start_time = time.time()




def testing():
	main('distance_matrix_test_case2.txt')
	print("--- %s seconds ---" % (time.time() - start_time))


testing()