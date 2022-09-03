import logging
import asyncio
import unittest
import multiprocessing
import time

from python.async_greeter_client import run
from python.async_greeter_server import serve

# Unittest for creating a drone
class TestDrone(unittest.TestCase):
    
    def test_drone(self):
        
        process_server = multiprocessing.Process(target=asyncio.run(serve()))
        process_server.start()
        # Give server time to start
        time.sleep(1)
        
        # Start drone
        process_drone = multiprocessing.Process(target=asyncio.run(run()))
        
        process_drone.start()
        time.sleep(10)
        
        processes = [process_server, process_drone]
        
        for process in processes:
            process.terminate()
            process.join()