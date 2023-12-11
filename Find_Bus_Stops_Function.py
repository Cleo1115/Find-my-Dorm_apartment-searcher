import contextily as ctx
import folium
import geopy.distance
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
from operator import itemgetter
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from geopy.geocoders import Nominatim
from geopy.point import Point

def Address_to_Location(address):
    """
        Convert the provided address to latitude and longitude coordinates.

        Parameters:
        - address (str): The address to be geocoded.

        Returns:
        - tuple: A tuple containing the latitude and longitude coordinates.

        Example:
        ```python
        location = Address_to_Location("1600 Amphitheatre Parkway, Mountain View, CA")
        print(location)  # Output: (37.423021, -122.083739)
        ```
    """
    full_address = address+', '+'IL'
    locator = Nominatim(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'")
    location = locator.geocode(full_address)
    latitude, longitude = location.latitude, location.longitude
    return latitude, longitude

def find_nearby_bus_stops(location, distance):
    """
        Find nearby bus stops within a specified distance from the given location.

        Parameters:
        - location (tuple): A tuple containing the latitude and longitude coordinates.
        - distance (float): The distance within which to search for bus stops.

        Returns:
        - folium.Map: A Folium map with markers for the start point, bus stops, and optimized bus routes.

        Example:
        ```python
        location = (40.11, -88.23)  # Example coordinates for an apartment near UIUC
        bus_map = find_nearby_bus_stops(location, distance=500)
        bus_map.save("bus_stops_map.html")
        ```
    """
    # Input the apartment/house's location (latitude, longtitude)
    DORM_LOCATION = location
    # Specify distance in meters
    DIST = 500
    # Specify the number of vehicles
    NUM_VEHICLES = 4
    # Get the highway graph
    G = ox.graph_from_point(DORM_LOCATION, dist=DIST, network_type='drive') 
    # Use the nearest node to the dorm location as the start
    start = ox.distance.nearest_nodes(G, DORM_LOCATION[1], DORM_LOCATION[0]) 
    # Find bus stops
    bus_stops = ox.features_from_point(DORM_LOCATION, {"highway": "bus_stop"}, dist=DIST)
    # Get the nearest nodes to bus stops
    bus_stop_nodes = list(map(itemgetter(1), bus_stops.index.values)) 
    # Combine start and bus_stops
    nodes = [start] + bus_stop_nodes
    # Add bus stops to the graph
    for index, bus_stop in bus_stops.iterrows(): 
        #Find nearest node of bus stop
        nearest_node = ox.distance.nearest_nodes(G, bus_stop.geometry.x, bus_stop.geometry.y) 
        distance = geopy.distance.distance((G.nodes[nearest_node]['y'], G.nodes[nearest_node]['x']), (bus_stop.geometry.y, bus_stop.geometry.x))
        # Add bus stop node
        G.add_node(index[1], x=bus_stop.geometry.x, y=bus_stop.geometry.y) 
        G.add_edge(index[1], nearest_node, weight=distance.m)
        G.add_edge(nearest_node, index[1], weight=distance.m)

    # Get edges as GeoDataFrames
    edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
    # Create the routing index manager
    manager = pywrapcp.RoutingIndexManager(len(nodes), NUM_VEHICLES, nodes.index(start))
    # Create routing model
    routing = pywrapcp.RoutingModel(manager)
    # Define distance callback
    def distance_callback(from_node_index, to_node_index):
        from_node = nodes[manager.IndexToNode(from_node_index)]
        to_node = nodes[manager.IndexToNode(to_node_index)]
        return nx.shortest_path_length(G, from_node, to_node)
    # Register distance callback
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(transit_callback_index, 0, 3000, True, dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)
    # Set path-cheapest-arc search strategy
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)
    total_distance = 0
    for vehicle_id in range(NUM_VEHICLES):
        index = routing.Start(vehicle_id)
        route_distance = 0
        route = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route.append(node_index)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        route.append(manager.IndexToNode(index))
        total_distance += route_distance
    m = folium.Map(location=DORM_LOCATION, zoom_start=16)
    # Plot start
    start_coords = (G.nodes[start]['y'], G.nodes[start]['x'])
    folium.Marker(location=start_coords, icon=folium.Icon(color='red', icon='home', prefix='fa'), tooltip=f"Start {start_coords}").add_to(m)

    # Plot bus stops
    for index, bus_stop in bus_stops.iterrows():
        stop_coords = (bus_stop.geometry.y, bus_stop.geometry.x)
        folium.Marker(location=stop_coords, icon=folium.Icon(color='green', icon='bus', prefix='fa'), tooltip=f"Bus Stop {stop_coords}").add_to(m)
    colors = ['orange', 'purple', 'brown', 'blue']
    # Plot routes
    for vehicle_id in range(NUM_VEHICLES):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route.append(nodes[node_index])
            index = solution.Value(routing.NextVar(index))
        route.append(nodes[manager.IndexToNode(index)])
        color = colors[vehicle_id % NUM_VEHICLES]
        # Create a list of line segments for the route
        segments = []
        for i in range(len(route)-1):
            # Get shortest path between nodes
            path = nx.shortest_path(G, route[i], route[i + 1], weight='length')
            # Add line segment to list
            segments.append([(G.nodes[node]['y'], G.nodes[node]['x']) for node in path])
        # Create polyline from line segments and add to map
        for segment in segments:
            folium.PolyLine(locations=segment, color=color, weight=5).add_to(m)
    # Return map
    return m  

def bus_stops_searcher(address, distance=500):
    """
        Search for nearby bus stops based on the provided address.

        Parameters:
        - address (str): The address for which to find nearby bus stops.
        - distance (float, optional): The distance within which to search for bus stops (default is 500 meters).

        Returns:
        - folium.Map: A Folium map with markers for the start point, bus stops, and optimized bus routes.

        Example:
        ```python
        bus_map = bus_stops_searcher("501 E. Healey", distance=500)
        bus_map.save("custom_bus_map.html")
        ```
    """
    location = Address_to_Location(address)
    bus_map = find_nearby_bus_stops(location, distance = 500)
    return bus_map

