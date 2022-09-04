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
        loop = asyncio.get_event_loop()

        future_server = asyncio.run_coroutine_threadsafe(serve(), loop)
        future_drone =  asyncio.run_coroutine_threadsafe(run(), loop)
        # Give server time to start
        
        time.sleep(10)
        result = future_server.result()
        result = future_drone.result()