# split this file 
path = '/home/dell/Desktop/OHW/interIITTechMeet/busStops.txt'

# into these 3 files
path_1 = '/home/dell/Desktop/OHW/interIITTechMeet/busStops_1.txt'
path_2 = '/home/dell/Desktop/OHW/interIITTechMeet/busStops_2.txt'
path_3 = '/home/dell/Desktop/OHW/interIITTechMeet/busStops_3.txt'

# Read the bus stops
allBusStopsFile = open(path, 'r')
allBusStops = list(allBusStopsFile)
allBusStopsFile.close()

# Size of each file
busStopsPerFile = len(allBusStops) // 3

# Open the files
allBusStopsFile_1 = open(path_1, 'w')
allBusStopsFile_2 = open(path_2, 'w')
allBusStopsFile_3 = open(path_3, 'w')

# counter
count = 0
# splitting
for busStop in allBusStops:

	if count < busStopsPerFile:
		allBusStopsFile_1.write(busStop)
	elif count < busStopsPerFile * 2:
		allBusStopsFile_2.write(busStop)
	else:
		allBusStopsFile_3.write(busStop)

	count+=1

# close all files
allBusStopsFile_1.close()
allBusStopsFile_2.close()
allBusStopsFile_3.close()

#########################################################################################

# print(allBusStops)
# print(type(allBusStops))
# print(len(allBusStops))

# if count > busStopsPerFile:
# 	break
# else:
# 	allBusStopsFile_1.write(busStop)

# count = count + 1

# allBusStopsFile_1.write('\n'.join(allBusStops[:busStopsPerFile]))
# allBusStopsFile_1.write(allBusStops[:busStopsPerFile])  # --> error
# allBusStopsFile_1.write(str(allBusStops[:busStopsPerFile]))  # --> ok, pretty bad
