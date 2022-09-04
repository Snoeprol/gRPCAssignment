import grpc

from unittest import IsolatedAsyncioTestCase

from python.helpers_client import Drone, register_drone
from python import dronecommander_pb2, dronecommander_pb2_grpc

CHANNEL = "localhost:50051"

# Unittest for creating a drone
class TestDrone(IsolatedAsyncioTestCase):
    
    async def test_drone_register(self):
        
        # Start the client
        async with grpc.aio.insecure_channel(CHANNEL) as channel:
            stub = dronecommander_pb2_grpc.DroneCommanderStub(channel)
            drone_id = await register_drone(stub)
            # Assert drone id is int
            assert isinstance(drone_id, int)
            
    async def test_send_position(self):
        
        # Start the client
        async with grpc.aio.insecure_channel(CHANNEL) as channel:
            stub = dronecommander_pb2_grpc.DroneCommanderStub(channel)
            
            # Set position
            drone = Drone(0, vis=False)
            drone.set_position()
            position_request = drone.position_to_position_request()
            position_reply = await stub.send_position(position_request)
            
            # Assert there was a reply
            assert position_reply is not None
            
    async def test_receive_location(self):
        async with grpc.aio.insecure_channel(CHANNEL) as channel:
            stub = dronecommander_pb2_grpc.DroneCommanderStub(channel)
            
            # Get position
            reply = stub.listen_waypoint(
                dronecommander_pb2.ListenWaypointRequest(id=0),
            )    
            async for response in reply:
                assert response is not None
                break