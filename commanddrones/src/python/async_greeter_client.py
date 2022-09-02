# Copyright 2021 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python AsyncIO implementation of the GRPC hellostreamingworld.MultiGreeter client."""

import asyncio
import logging
import grpc
import dronecommander_pb2
import dronecommander_pb2_grpc
import random

from helpers import gen_random_position, gen_new_position, register_drone

async def send_location(stub, pingtime, drone_id):
    position = gen_random_position()
    while True:
        
        position = gen_new_position(position)
        position_request = dronecommander_pb2.SendpositionRequest(position=position, id=drone_id)
        stub.send_position(position_request)
        print('Sending position')
        await asyncio.sleep(pingtime)

async def receive_location(stub, drone_id):
    # May be stuck here if no waypoint is given for a while
    async for response in stub.listen_waypoint(
        dronecommander_pb2.ListenWaypointRequest(id=drone_id)
    ):  
        print(
            f"Moving drone to waypoint: lat {response.waypoint.lat:.2f}, lon {response.waypoint.lon:.2f}",
        )

async def run(pingtime=5) -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = dronecommander_pb2_grpc.DroneCommanderStub(channel)
        
        # Register drone
        drone_id = await register_drone(stub)
        
        # Start sending position and receiving locations
        t1 = asyncio.create_task(send_location(stub, pingtime, drone_id))
        t2 = asyncio.create_task(receive_location(stub, drone_id))
        
        await asyncio.gather(t1, t2)


if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(run())
