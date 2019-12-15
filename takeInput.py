import os

def main(ifile = 'input.txt', refined_input_file, demands_file):
	

	f = open(ifile, 'r')
	inparr = f.readlines()
	#print(inparr)
	"""
	Assuming input file consists of lines of :
	<S.No> <Person_id> <Bus_stop_name>

	"""
	count = {} #Map of bus_stop:load
	for i in inparr:
		#print(i)
		#extract bus stop names from file
		j = i.split()
		j = j[2:]
		j = "+".join(j)

		#Update map
		if j in count:
			count[j] += 1
		else:
			count[j] = 1

	#print(count)

	f.close()

	f2 = open(refined_input_file, 'w')
	f3 = open(demands_file, 'w')

	f3.write("0 \n") #Bosch Bidadi office's demand is 0
	for i in count:
		f2.write(i + " " + str(count[i]) + "\n")
		f3.write(str(count[i]) + "\n")

	f2.close()
	f3.close()

	return(count)
