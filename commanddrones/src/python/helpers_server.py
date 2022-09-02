import random
import json
import dronecommander_pb2
import os
import warnings

FILE_LOC = r'..\data\paths.json'

class RouteGenerator:
    
    def __init__(self, fileloc=FILE_LOC) -> None:
        """
        Initialize the route generator.
        
        :return: None.
        """
        self.FILE_LOC = fileloc

        # Check that file in FILE_LOC is smaller than 10 MB
        if os.path.getsize(self.FILE_LOC) > 10e6:
            warnings.warn('File is large and may take a while to load.')
        self.routes = json.load(open(self.FILE_LOC, 'r', encoding='utf-8'))
        self.num_routes = len(self.routes['features'])
        
    def gen_route(self):
        """
        Picks a random route from the list of routes.
        
        :return: A random route.
        """
        route_id = random.randint(0, self.num_routes - 1)
        route = self.routes['features'][route_id]['geometry']['coordinates']
        return route, route_id

def point_to_waypoint(point):
    """
    Convert a point to a waypoint.
    
    :param point: The point to convert.
    :return: The waypoint.
    """
    lon = point[0]
    lat = point[1]
    return dronecommander_pb2.Waypoint(lat=lat, lon=lon)