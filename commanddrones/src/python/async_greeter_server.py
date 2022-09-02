"""The Python AsyncIO implementation of the GRPC Dronecommander server."""

import asyncio
import logging
import dronecommander_pb2
import dronecommander_pb2_grpc
import grpc

import numpy as np

from helpers import gen_route

NUMBER_OF_REPLY = 10

def gen_random_waypoint():
    lon = np.random.uniform(-180, 180)
    lat = np.random.uniform(-90, 90)
    return dronecommander_pb2.Waypoint(lat=lat, lon=lon)

def point_to_waypoint(point):
    lon = point[0]
    lat = point[1]
    return dronecommander_pb2.Waypoint(lat=lat, lon=lon)

class DroneCommander(dronecommander_pb2_grpc.DroneCommanderServicer):
    
    def __init__(self) -> None:
        self._count = 0
        
    def register(self, request, context):
        self._count += 1
        drone_id = self._count
        print(f"Registering drone with id {drone_id}")
        return dronecommander_pb2.RegisterReply(id=drone_id)
    
    async def listen_waypoint(self, request, context):
        drone_id = request.id
        route, route_id = gen_route()
        print(f"Giving route {route_id} to drone {drone_id}")
        for point in route:
            waypoint = point_to_waypoint(point)
            waypoint_reply = dronecommander_pb2.ListenWaypointReply(waypoint=waypoint)
            print(f"Yielding position to drone {drone_id}.")
            await asyncio.sleep(10)
            yield waypoint_reply
    
    def send_position(self, request, context):
        print(f"Position ping received from drone {request.id}")   
        return dronecommander_pb2.SendpositionReply()

async def serve() -> None:
    server = grpc.aio.server()
    dronecommander_pb2_grpc.add_DroneCommanderServicer_to_server(DroneCommander(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info(f"Starting server on {listen_addr}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
