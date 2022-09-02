import random
import json
import dronecommander_pb2

FILE_LOC = r'..\data\paths.json'

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
    
def gen_route():
    # Should only be done with small files
    routes = json.load(open(FILE_LOC, 'r', encoding='utf-8'))
    num_routes = len(routes['features'])
    route_id = random.randint(0, num_routes - 1)
    route = routes['features'][route_id]['geometry']['coordinates']
    return route, route_id

async def register_drone(stub):
    register_request = dronecommander_pb2.RegisterRequest(name='killer-drone-69')
    response = stub.register(register_request)
    await response
    drone_id = response._invocation_task.result().id
    return drone_id