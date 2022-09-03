"""The Python AsyncIO implementation of the GRPC Dronecommander server."""

import asyncio
import logging
import dronecommander_pb2
import dronecommander_pb2_grpc
import grpc

import numpy as np

from helpers_server import RouteGenerator, point_to_waypoint

HOST_ADRESS = "[::]:50051"

class DroneCommander(dronecommander_pb2_grpc.DroneCommanderServicer):
    
    def __init__(self) -> None:
        """
        Initialize the server.
        
        :return: None.
        """
        self._count = 0
        self.route_generator = RouteGenerator()
        
    def register(self, request, context):
        """
        Register a drone at the server.
        
        :param request: The request object.
        :param context: The context object.
        :return: A drone id.
        """
        self._count += 1
        drone_id = self._count
        print(f"Registering drone with id {drone_id}")
        return dronecommander_pb2.RegisterReply(id=drone_id)
    
    async def listen_waypoint(self, request, context):
        """
        Sends waypoints to the drone.
        
        :param request: The request object.
        :param context: The context object.
        :return: A yield of waypoints.
        """
        drone_id = request.id
        route, route_id = self.route_generator.gen_route()
        print(f"Giving route {route_id} to drone {drone_id}")
        for point in route:
            waypoint = point_to_waypoint(point)
            waypoint_reply = dronecommander_pb2.ListenWaypointReply(waypoint=waypoint)
            print(f"Yielding position to drone {drone_id}.")
            await asyncio.sleep(10)
            yield waypoint_reply
    
    def send_position(self, request, context):
        """
        Receives a position of the drone and returns an empty response.
        
        :param request: The request object.
        :param context: The context object.
        :return: An empty response.
        """
        print(f"Position ping received from drone {request.id}")   
        return dronecommander_pb2.SendpositionReply()

async def serve() -> None:
    """
    Start the server.
    
    :return: None
    """
    server = grpc.aio.server()
    dronecommander_pb2_grpc.add_DroneCommanderServicer_to_server(DroneCommander(), server)
    server.add_insecure_port(HOST_ADRESS)
    logging.info(f"Starting server on {HOST_ADRESS}.")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
