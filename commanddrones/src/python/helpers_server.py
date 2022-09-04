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

        self.routes = self.load_routes()
        self.num_routes = len(self.routes['features'])
    
    def load_routes(self):
        """
        Loads routes from a json file.
        
        :return: A list of routes.
        """
        with open(self.FILE_LOC, 'r', encoding='utf-8') as f:
            routes = json.load(f)
        return routes
    
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

def points_to_plot_format(points):
    """
    Makes the points in the positions list into two lists
    suitable for plotting.
    
    :return: Two lists, one with the lats and one with the lons.
    """
    points_lat = []
    points_lon = []
    
    for point in points:
        points_lat.append(point.lat)
        points_lon.append(point.lon)
    return points_lat, points_lon

def check_vis(reporting_period, positions, drone_id):
    """
    Check if visualization is on, and plot if the reporting period is met.
    
    :return: None.
    """
    if len(positions) % reporting_period == 0:
        visualize_path(positions, len(positions), drone_id)

def visualize_path(points, path_number, drone_id):
    """
    If the visualization is on, plot the path of the drone.
    
    :return: None
    """
    import matplotlib.pyplot as plt
    lats, lons = points_to_plot_format(points)
    plt.plot(lats, lons, c='r', marker='o')
    
    # Plot text with start and end point
    plt.text(lats[0], lons[0], 'Start', fontsize=10)
    plt.text(lats[-1], lons[-1], 'End', fontsize=10)
    plt.grid()
    im_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
                '..', fr"data\drone_{drone_id}_path_{path_number}.png"))
    plt.savefig(im_path, dpi=300)
    plt.clf()