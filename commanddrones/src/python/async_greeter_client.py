
"""The Python AsyncIO implementation of the GRPC Dronecommander client."""

import asyncio
import grpc

from dronecommander_pb2 import ListenWaypointRequest
from dronecommander_pb2_grpc import DroneCommanderStub
from helpers_client import Drone, register_drone

CHANNEL = "localhost:50051"

async def send_location(stub, pingtime, drone):
    """
    Streams the position of the drone to the server.
    
    :param stub: The stub object.
    :param pingtime: The time between sending positions.
    :param drone: The drone.
    :return: None.
    """
    while True:
        drone.set_position()
        position_request = drone.position_to_position_request()
        stub.send_position(position_request)
        print('Pinged server')
        await asyncio.sleep(pingtime)

async def receive_location(stub, drone):
    """
    Accepts a location from the server and sends the drone to that location.
    
    :param stub: The stub object.
    :param drone: The drone.
    :return: None.
    """
    async for response in stub.listen_waypoint(
        ListenWaypointRequest(id=drone.id),
    ):  
        print(
            f"Starting path to: lat {response.waypoint.lat:.3f}, lon {response.waypoint.lon:.3f}",
        )
        drone.set_target(response.waypoint)

async def run(pingtime=5) -> None:
    """
    Starts the client and connect over gRPC.
    
    :param pingtime: The time between sending positions.
    :return: None.
    """
    async with grpc.aio.insecure_channel(CHANNEL) as channel:
        stub = DroneCommanderStub(channel)
        
        # Register drone
        drone_id = await register_drone(stub)
        drone = Drone(drone_id, vis=True)
        
        # Start sending position and receiving locations
        t1 = asyncio.create_task(send_location(stub, pingtime, drone))
        t2 = asyncio.create_task(receive_location(stub, drone))
        
        await asyncio.gather(t1, t2)


if __name__ == "__main__":
    asyncio.run(run())
