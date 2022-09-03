import random
import time
import dronecommander_pb2
import plotly.express as px
import pandas as pd

def gen_random_waypoint():
    lon = random.uniform(-180, 180)
    lat = random.uniform(-90, 90)
    return dronecommander_pb2.Waypoint(lat=lat, lon=lon)

def gen_new_position(location):
    lat = location.lat + random.uniform(-0.01, 0.01)
    lon = location.lon + random.uniform(-0.01, 0.01)
    alt = location.alt + random.uniform(-0.01, 0.01)
    return dronecommander_pb2.Position(lat=lat, lon=lon, alt=alt)

def gen_random_position():
    # User random to generate
    lon = random.uniform(-180, 180) 
    lat = random.uniform(-90, 90)
    alt = random.uniform(0, 100)
    return dronecommander_pb2.Position(lat=lat, lon=lon, alt=alt)

def move_to_waypoint(waypoint):
    print(
        f"Moving to waypoint: lat {waypoint.lat}, lon {waypoint.lon}"
    )

async def register_drone(stub):
    register_request = dronecommander_pb2.RegisterRequest(name='killer-drone-69')
    response = stub.register(register_request)
    await response
    drone_id = response._invocation_task.result().id
    return drone_id

class Drone:
    
    def __init__(self, drone_id):
        self.positions = []
        self.id = drone_id
        self.position = None
        self.target = None
        self.time_since_target = None
        self.target_time = time.time()
        
    def set_target(self, target):
        self.target = target
        self.target_time = time.time()
        
    def set_position(self, position):
        self.positions.append(position)
        self.position = position
        self.time_since_target = time.time() - self.target_time
        if len(self.positions) == 10:
            self._visualize_path()
    
    def _points_to_plot_format(self):
        points_lat = []
        points_lon = []
        
        for point in self.positions:
            points_lat.append(point.lat)
            points_lon.append(point.lon)
        return points_lat, points_lon
    
    def _visualize_path(self):
        import matplotlib.pyplot as plt
        points_x, points_y = self._points_to_plot_format()

        df = pd.DataFrame({"lat": points_x, "lon": points_y})
        print(df)
        fig = px.scatter_geo(df,lat='lat',lon='lon', color='lat')
        fig.update_layout(
        title = 'World',
        geo = dict(
            scope='europe',
            showland = True
        ))
        fig.write_image(fr"..\data\drone_{self.id}_path.png")