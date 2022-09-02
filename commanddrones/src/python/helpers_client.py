import random
import dronecommander_pb2

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
        self.id = drone_id
        self.position = None
        self.target = None
    
    def set_target(self, target):
        self.target = target
        
    def set_position(self, position):
        self.position = position
    
    