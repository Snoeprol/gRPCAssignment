import random
import time
import os
import dronecommander_pb2

from dataclasses import dataclass
from geopy.distance import geodesic as GD

# Speed of drone in m/s
SPEED = 5
REPORTING_PERIOD = 10
    
def gen_random_waypoint():
    """
    Generates a random waypoint.
    
    :return: The waypoint.
    """
    lon = random.uniform(-180, 180)
    lat = random.uniform(-90, 90)
    return dronecommander_pb2.Waypoint(lat=lat, lon=lon)

def gen_new_position(location):
    """
    Generates a new position based on the current position.
    
    :param location: The current position.
    :return: The new position.
    """
    lat = location.lat + random.uniform(-0.01, 0.01)
    lon = location.lon + random.uniform(-0.01, 0.01)
    alt = location.alt + random.uniform(-0.01, 0.01)
    return dronecommander_pb2.Position(lat=lat, lon=lon, alt=alt)

def gen_random_position():
    """
    Generates a random position.
    
    :return: The position.
    """
    # User random to generate
    lon = random.uniform(-180, 180) 
    lat = random.uniform(-90, 90)
    alt = random.uniform(0, 100)
    return dronecommander_pb2.Position(lat=lat, lon=lon, alt=alt)

def move_to_waypoint(waypoint):
    """
    Moves the drone to the waypoint.
    """
    print(
        f"Moving to waypoint: lat {waypoint.lat}, lon {waypoint.lon}"
    )

def point_to_send_position_request(point, drone_id):
        """
        Converts the point to a position request.
        
        :return: The position request.
        """
        return dronecommander_pb2.SendpositionRequest(
            id=drone_id,
            position=dronecommander_pb2.Position(
                lat=point.lat,
                lon=point.lon,
                alt=point.alt
            )
        )

async def register_drone(stub):
    """
    Registers the drone with the server.
    
    :param stub: The stub object.
    :return: The drone id.
    """
    register_request = dronecommander_pb2.RegisterRequest(name='killer-drone-69')
    response = stub.register(register_request)
    await response
    drone_id = response._invocation_task.result().id
    return drone_id

@dataclass
class Point:
    """
    Represents a 3D point in space
    """
    lon : float
    lat : float
    alt : float = 0
                      
class Drone:

    def __init__(self, drone_id, vis=False):
        self.positions = []
        self.id = drone_id
        self.speed = SPEED
        self.vis = vis
        
        # Start in middle of Amsterdam
        self.position = Point(lat=52.37817152269896, lon=4.8997896909713745, alt = 10)
        self.target = None
        self.time_since_target = None
        self.target_time = time.time()
    
    def position_to_position_request(self):
        """
        Makes the drone position into a position request.
        
        :return: The position request.
        """
        return point_to_send_position_request(self.position, self.id)
     
    def set_target(self, target):
        """
        Set the target of the drone.
        
        :param target: The target.
        :return: None
        """
        self.target = Point(target.lat, target.lon)
        self.target_time = time.time()
        
    def set_position(self):
        """
        Change the position of the drone based on the target
        and the time since the target was set.
        
        :return: None
        """
        if self.target == None:
            pass
        else:
            self.time_since_target = time.time() - self.target_time

            target_lon = self.target.lon
            target_lat = self.target.lat
            
            pos_lon = self.position.lon
            pos_lat = self.position.lat
            
            dist_traveled = SPEED * self.time_since_target
            dist_to_target = self.lon_lat_to_dist(pos_lon, pos_lat, target_lon, target_lat)
                
            self.target_time = time.time()
            
            # Drone has reached target already
            if dist_traveled > dist_to_target:
                self.position = self.target
            
            # Calculate how much the drone has moved
            else:  
                frac_traveled = dist_traveled / dist_to_target
            
                new_lon = pos_lon + frac_traveled * (target_lon - pos_lon)
                new_lat = pos_lat + frac_traveled * (target_lat - pos_lat)
                
                self.position = Point(lat=new_lat, lon=new_lon)
            
            self.positions.append(self.position)
            
            if len(self.positions) % REPORTING_PERIOD == 0 and self.vis:
                path_number = len(self.positions) // REPORTING_PERIOD
                self._visualize_path(path_number)
        
    def _points_to_plot_format(self):
        """
        Makes the points in the positions list into two lists
        suitable for plotting.
        
        :return: Two lists, one with the lats and one with the lons.
        """
        points_lat = []
        points_lon = []
        
        for point in self.positions:
            points_lat.append(point.lat)
            points_lon.append(point.lon)
        return points_lat, points_lon
    
    def _visualize_path(self, path_number):
        """
        If the visualization is on, plot the path of the drone.
        
        :return: None
        """
        import matplotlib.pyplot as plt
        lats, lons = self._points_to_plot_format()
        plt.plot(lats, lons, c='r', marker='o')
        
        # Plot text with start and end point
        plt.text(lats[0], lons[0], 'Start', fontsize=10)
        plt.text(lats[-1], lons[-1], 'End', fontsize=10)
        plt.grid()
        im_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', fr"data\drone_path_{path_number}.png"))
        plt.savefig(im_path, dpi=300)
        plt.clf()
    
    def lon_lat_to_dist(self, lon1, lat1, lon2, lat2):
        """
        Calculate the distance between two points in meters.
        
        :param lon1: Longitude of point 1.
        :param lat1: Latitude of point 1.
        :param lon2: Longitude of point 2.
        :param lat2: Latitude of point 2.
        :return: The distance in meters.
        """
        return GD((lat1, lon1), (lat2, lon2)).meters