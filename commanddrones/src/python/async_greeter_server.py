"""The Python AsyncIO implementation of the GRPC Dronecommander server."""

import asyncio
import logging
import grpc

from dronecommander_pb2 import RegisterReply, ListenWaypointReply, SendpositionReply
from  dronecommander_pb2_grpc import DroneCommanderServicer, add_DroneCommanderServicer_to_server
from helpers_server import RouteGenerator, point_to_waypoint, visualize_path, check_vis

HOST_ADRESS = "[::]:50051"
REPORTING_PERIOD = 10

class DroneCommander(DroneCommanderServicer):
    
    def __init__(self, vis=False) -> None:
        """
        Initialize the server.
        
        :return: None.
        """
        self._count = 0
        self.route_generator = RouteGenerator()
        self.positions = {}
        self.vis = vis
        
    def register(self, request, context):
        """
        Register a drone at the server.
        
        :param request: The request object.
        :param context: The context object.
        :return: A drone id.
        """
        self._count += 1
        drone_id = self._count
        logging.info(f"Registering drone with id {drone_id}")
        self.positions[drone_id] = []
        return RegisterReply(id=drone_id)
    
    async def listen_waypoint(self, request, context):
        """
        Sends waypoints to the drone.
        
        :param request: The request object.
        :param context: The context object.
        :return: A yield of waypoints.
        """
        drone_id = request.id
        route, route_id = self.route_generator.gen_route()
        logging.info(f"Giving route {route_id} to drone {drone_id}")
        for point in route:
            waypoint = point_to_waypoint(point)
            waypoint_reply = ListenWaypointReply(waypoint=waypoint)
            logging.info(f"Yielding position to drone {drone_id}.")
            yield waypoint_reply
            await asyncio.sleep(10)
    
    def send_position(self, request, context):
        """
        Receives a position of the drone and returns an empty response.
        
        :param request: The request object.
        :param context: The context object.
        :return: An empty response.
        """
        drone_id = request.id
        self.positions[drone_id].append(request.position)

        # Visualize path
        if self.vis:
            check_vis(REPORTING_PERIOD, self.positions[drone_id], drone_id)

        logging.info(f"Position ping received from drone {drone_id}")   
        return SendpositionReply()

async def serve() -> None:
    """
    Start the server.
    
    :return: None
    """
    server = grpc.aio.server()
    add_DroneCommanderServicer_to_server(DroneCommander(vis=True), server)
    server.add_insecure_port(HOST_ADRESS)
    logging.info(f"Starting server on {HOST_ADRESS}.")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
