# BOSCH_Route_Optimization_Algorithm

### AGENDA
1.) To develop a route optimization algorithm that caters to the real time changing demand of customers to determine route and schedule of buses depending on the constraints provided.    
2.) The algorithm should be able to give optimized routes for ‘n’ number of constraints , for example the desired output should be achieved with either one of the constraints as well as considering all of them together as per the requirements.      
3.) Justification and visualization of the method.


### CONSTRAINTS
* Time window for pick up and drop off
* Minimize operational cost
* Number of buses
* Vehicle occupancy should be at least 85%

### INFERENCE

We understood the following from the given sample data and solution:
  * The data will be given as an array of passenger_name:bus_stop_name
  * There will be two sets of data, one for each of the following :
    * Pickup 
    * Drop back
  * We need to determine and visualize the best routes to be followed by each of the buses for the to and fro travelling between Bosch       Office and each of the input bus stops (considering the above mentioned constraints).
  
## THE PLAN

* Task 1:
   - Get all the bus stop names in Bangalore Geographical Area by scraping data off [here](https://narasimhadatta.info/bmtc_query.html).
* Task 2:
   - Find out the gps coordinates of all the bus stops by web scraping.
* Task 3:
   - Get the fastest routes/distances between each pair of stops.
   - We use the Open Source Routing Machine's (OSRM) [table service](https://github.com/Project-OSRM/osrm-backend/blob/master/docs/http.md#table-service) to fill the distance_matrix that contains the above information.
* Task 4:
   - Once we know all-source-all-destination shortest paths, we take the given input points and then use the constraint vehicle routing      methods with slight modifications, to get the minimum number of buses needed to cover all the places and reach the Bosch office. 
   - There are various methods to solve the VRP. The algorithms about which we have researched have been mentioned in the [resources.md](https://github.com/Hrishabh-yadav/BOSCH_Route_Optimization_Algorithm/blob/master/Resources.md)        file.         
   - We will try out all the approaches and determine the best one for our case.
* Task 5:
   - After getting the optimized number of buses and also their routes, we visualize it using Python's Network Graph library -NetworkX.
