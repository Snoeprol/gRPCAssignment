
"""The Python AsyncIO implementation of the GRPC Dronecommander client."""

import asyncio
import logging
import grpc
import dronecommander_pb2
import dronecommander_pb2_grpc

from helpers_client import gen_random_position, gen_new_position, register_drone
from helpers_client import Drone

import time

timer = time.time()

async def send_location(stub, pingtime, drone):
    """
    Streams the position of the drone to the server.
    
    :param stub: The stub object.
    :param pingtime: The time between sending positions.
    :param drone: The drone.
    :return: None.
    """
    position = gen_random_position()
    while True:
        global timer
        position = gen_new_position(position)
        position_request = dronecommander_pb2.SendpositionRequest(position=position, id=drone.id)
        stub.send_position(position_request)
        print(timer - time.time())
        timer = time.time()
        
        drone.set_position(position)
        print('Sending position')
        await asyncio.sleep(pingtime)

async def receive_location(stub, drone):
    """
    Accepts a location from the server and moves the drone to that location.
    
    :param stub: The stub object.
    :param drone: The drone.
    :return: None.
    """
    # May be stuck here if no waypoint is given for a while
    async for response in stub.listen_waypoint(
        dronecommander_pb2.ListenWaypointRequest(id=drone.id)
    ):  
        print(
            f"Moving drone to waypoint: lat {response.waypoint.lat:.2f}, lon {response.waypoint.lon:.2f}",
        )
        drone.set_target(response.waypoint)

async def run(pingtime=2) -> None:
    """
    Starts the client and connect over gRPC.
    
    :param pingtime: The time between sending positions.
    :return: None.
    """
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = dronecommander_pb2_grpc.DroneCommanderStub(channel)
        
        # Register drone
        drone_id = await register_drone(stub)
        drone = Drone(drone_id)
        
        # Start sending position and receiving locations
        t1 = asyncio.create_task(send_location(stub, pingtime, drone))
        t2 = asyncio.create_task(receive_location(stub, drone))
        
        await asyncio.gather(t1, t2)


if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(run())
