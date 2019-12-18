from __future__ import print_function
import os
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import time
import random
from tabulate import tabulate
start_time = time.time()

def getdata(input_file):
    file = open(input_file,'r')
    w = file.readlines()
    for i in range(len(w)):
        w[i]=w[i].split()
        for j in range(len(w[i])):
            w[i][j]=float(w[i][j])
    ans =[]
    dupe = [0]*(len(w[0]) +1)
    for i in w:
        i.append(0)
        ans.append(i)
    ans.append(dupe)
    return ans

def getdemands(demand_file):
    arr=[]
    f = open(demand_file,'r')
    f = f.readlines()
    for i in f:
        arr.append(int(i))
    arr.append(0)
    return arr

def get_sum(data):
    sum = 0
    for i in data['demands']:
        sum += i
    return sum
    
def create_data_model(input_file, demand_file):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = getdata(input_file)
    data['demands'] = getdemands(demand_file)
    data['demand_sum'] = get_sum(data)
    data['num_vehicles'] = data['demand_sum']//36-1
    return data

def find_details(data, manager, routing, assignment):
    total_distance = 0
    loads =[]
    algo_data = {}
    algo_data['Route'] = []
    algo_data['total_distance'] = -1
    algo_data['load'] = []
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        route_distance = 0
        route_load = 0
        bus_route = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            bus_route.append(node_index)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        total_distance += route_distance
        loads.append(route_load)
        algo_data['Route'].append(bus_route)
        algo_data['load'].append(route_load)
    algo_data['total_distance'] = total_distance
    return algo_data


def print_solution(data, manager, routing, assignment):
    """Prints assignment on console."""
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]

            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))

def algo_type(algo_num):
    if algo_num == 0:
        return routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    elif algo_num == 1:
        return routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC
    elif algo_num == 2:
        return routing_enums_pb2.FirstSolutionStrategy.PATH_MOST_CONSTRAINED_ARC
    elif algo_num == 3:
        return routing_enums_pb2.FirstSolutionStrategy.SAVINGS
    elif algo_num == 4:
        return routing_enums_pb2.FirstSolutionStrategy.SWEEP
    elif algo_num == 5:
        return routing_enums_pb2.FirstSolutionStrategy.BEST_INSERTION
    elif algo_num == 6:
        return routing_enums_pb2.FirstSolutionStrategy.CHRISTOFIDES
    elif algo_num == 7:
        return routing_enums_pb2.FirstSolutionStrategy.ALL_UNPERFORMED
    elif algo_num == 8:
        return routing_enums_pb2.FirstSolutionStrategy.LOCAL_CHEAPEST_ARC
    elif algo_num == 9:
        return routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
    elif algo_num == 10:
        return routing_enums_pb2.FirstSolutionStrategy.FIRST_UNBOUND_MIN_VALUE

def calculate_priority(algo_data, operational_cost, price_km, vehicle_capacities ):
    _buses_with_85 = 0
    num_buses  = 0
    total_cost = 0
    for i in algo_data['load']:
        if i >= float(vehicle_capacities)*0.85:
            _buses_with_85 +=1
        if i > 0:
            num_buses += 1
    return (num_buses * operational_cost + algo_data['total_distance']/1000*price_km , _buses_with_85)


def main(input_file, demand_file, operational_cost, price_km):
    # Instantiate the data problem.
    print("Algo_starts_running")
    print("\n--------------------------------------------------------------------------------------\n")
    data = create_data_model(input_file, demand_file)
   # Setting first solution heuristic.
    ALl_algo_data = {}
    inf  = 9999999999999999
    val = 0
    for j in range(0,1):
        if len(data['distance_matrix']) >= 1000 and len(ALl_algo_data) == 0:
            data['num_vehicles'] += 4
        elif  len(ALl_algo_data) == 0:
            data['num_vehicles'] += 2
        data['vehicle_capacities'] = [] 
        for i in range(0,data['num_vehicles']):
            data['vehicle_capacities'].append(32)
        data['starts'] = [0]*data['num_vehicles']
        data['ends'] = [len(data['distance_matrix'])-1]*data['num_vehicles']

        for i in range(0,4):
            algo_data = {}
            algo_data['Route'] = []
            algo_data['total_distance'] = -1
            algo_data['load'] = []
            algo_data['priority'] = (inf, 0)
            try:
                start_time = time.time() 
                manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['starts'], data['ends'])
                routing = pywrapcp.RoutingModel(manager)

               # Create and register a transit callback.
                def distance_callback(from_index, to_index):
                    """Returns the distance between the two nodes."""
                    # Convert from routing variable Index to distance matrix NodeIndex.
                    from_node = manager.IndexToNode(from_index)
                    to_node = manager.IndexToNode(to_index)
                    return data['distance_matrix'][from_node][to_node]

                transit_callback_index = routing.RegisterTransitCallback(distance_callback)
                routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

                # Add Distance constraint.
                dimension_name = 'Distance'
                routing.AddDimension(
                    transit_callback_index,
                    0,  # no slack
                    70000,  # vehicle maximum travel distance
                    True,  # start cumul to zero
                    dimension_name)
                distance_dimension = routing.GetDimensionOrDie(dimension_name)
                ##distance_dimension.SetGlobalSpanCostCoefficient(100000)
                 # Add Capacity constraint.
                def demand_callback(from_index):
                    """Returns the demand of the node."""
                    # Convert from routing variable Index to demands NodeIndex.
                    from_node = manager.IndexToNode(from_index)
                    return data['demands'][from_node]

                demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
                routing.AddDimensionWithVehicleCapacity(
                    demand_callback_index,
                    0,  # null capacity slack
                    data['vehicle_capacities'],  # vehicle maximum capacities
                    True,  # start cumul to zero
                    'Capacity')

                
                
                search_parameters = pywrapcp.DefaultRoutingSearchParameters()
                search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
                search_parameters.first_solution_strategy = (algo_type(i))
                if len(data['distance_matrix']) >= 1000:
                    search_parameters.time_limit.seconds = 10
                elif len(data['distance_matrix']) >= 100:
                    search_parameters.time_limit.seconds = 5
                else:
                    search_parameters.time_limit.seconds = 1
                # Solve the problem.
                assignment = routing.SolveWithParameters(search_parameters)
                #print(assignment)
                #print_solution(data, manager, routing, assignment)

                
                algo_data = find_details(data, manager, routing, assignment)
                algo_data['priority'] = calculate_priority(algo_data, operational_cost, price_km, data['vehicle_capacities'][0])
                ALl_algo_data[val] = algo_data
                val += 1
                
                # Print solution on console.
                print("Algorithm " + str(i) +" time: "+ str(time.time()-start_time))
                print("\n---------------------------------------------------------------------------------------\n")
            except (AttributeError, SystemError): 
                print("Algorithm "+ str(i) + ": Error AttributeError")
                print("\n---------------------------------------------------------------------------------------\n")
                break

    min_route = {}
    min_prioirty =(inf, inf)
    for i in ALl_algo_data:
        if ALl_algo_data[i]['priority'] < min_prioirty:
            min_prioirty = ALl_algo_data[i]['priority']
            min_route = ALl_algo_data[i]
    nodes_name = open('All_stop_1.txt','r').readlines()
    route_data = open("route_data",'w')
    visualization_data = open('visual_data.txt','w')
    long_lat = open('lat_long.txt', 'r').readlines()
    geocdes = []
    for i in long_lat:
        geocdes.append(i.split())
    bus_count = 1

    for bus_list in min_route['Route']:
        print("Route for Bus {0}: ".format(bus_count))
        route_data.write("Route for Bus {0}:\n".format(bus_count))
        visual_d = ""
        Bus_data = []
        prev_dis = 0
        prev_time = 0
        prev = len(data['distance_matrix'])-1
        for i in range(0,len(bus_list)):
            Bus_data.append([nodes_name[i][:len(nodes_name[i])-1], prev_dis + (data['distance_matrix'][prev][bus_list[i]]/1000),  (prev_time+ ((data['distance_matrix'][prev][bus_list[i]]/45000)*60))])
            visual_d += geocdes[i][0] + "," + geocdes[i][1] + " "
            prev_dis += (data['distance_matrix'][prev][bus_list[i]]/1000)
            prev_time += ((data['distance_matrix'][prev][bus_list[i]]/45000)*60)
            prev  = bus_list[i]
        print(tabulate(Bus_data, headers = ['Bus stand Name', 'Distance Travelled (km)', 'Time Taken(min)']))

        route_data.write(tabulate(Bus_data, headers = ['Bus stand Name', 'Distance Travelled (km)', 'Time Taken(min)']))
        route_data.write("\n")
        visualization_data.write(visual_d + '\n')
        bus_count += 1



        
