from __future__ import print_function
import os
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import time
import random
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

def getdemands(n, demands_file):
    """
    For random data,
    uncomment the commented part, and vice versa
    """

    f = open(demands_file,'r')
    arr = (f.read()).split()
    for i in range(0,n-1):
        #arr.append(random.randint(5,10)) #uncomment for random data
        arr[i] = int(arr[i])
    arr = arr[:n-1]
    arr[0] = 0
    """
    #Uncomment for random data
    arr=[0] 
    for i in range(0,n-1):
        arr.append(random.randint(5,10)) 
    """
    return arr


def get_sum(data):
    sum = 0
    for i in data['demands']:
        sum += i
    return sum
    
def create_data_model(input_file, demands_file):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = getdata(input_file)
    data['demands'] = getdemands(len(data['distance_matrix']), demands_file)
    data['demand_sum'] = get_sum(data)
    data['num_vehicles'] = data['demand_sum']//36+20
    data['vehicle_capacities'] = [] 
    for i in range(0,data['num_vehicles']):
        data['vehicle_capacities'].append(36)
    data['starts'] = [0]*data['num_vehicles']
    data['ends'] = [len(data['distance_matrix'])-1]*data['num_vehicles']
    return data

def find_details(data, manager, routing, assignment):
    total_distance = 0
    loads =[]
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        total_distance += route_distance
        loads.append(route_load)
    print(loads)
    print('Total distance of all routes: {}m'.format(total_distance))
    


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

def main(input_file, demands_file):
    # Instantiate the data problem.
    print("Algo_starts_running")
    print("\n--------------------------------------------------------------------------------------\n")
    data = create_data_model(input_file)
        
    # Setting first solution heuristic.
    for i in range(0,4):
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
                67000,  # vehicle maximum travel distance
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
            search_parameters.time_limit.seconds = 120
            # Solve the problem.
            assignment = routing.SolveWithParameters(search_parameters)
            #print(assignment)
            #print_solution(data, manager, routing, assignment)
            
            find_details(data, manager, routing, assignment)
            # Print solution on console.
            print("Algorithm " + str(i) +" time: "+ str(time.time()-start_time))
            print("\n---------------------------------------------------------------------------------------\n")
        except AttributeError: 
            print("Algorithm "+ str(i) + ": Error AttributeError")
            print("\n---------------------------------------------------------------------------------------\n")
        

if __name__ == '__main__':
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
