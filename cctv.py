#!/usr/bin/python3

from signal import pause
from buildhat import Motor, DistanceSensor
import time
from picamera import PiCamera
import pyshine as ps

HTML="""
<html>
<head>
<title>PyShine Live Streaming</title>
</head>

<body>
<center><h1> PyShine Live Streaming using PiCamera </h1></center>
<center><img src="stream.mjpg" width='640' height='480' autoplay playsinline></center>
</body>
</html>
"""


class Cctv:
    motor = Motor('A')
    motor.set_default_speed(5)
    dist = DistanceSensor('B', threshold_distance=100)
    
    def __init__(self):
        self.motor.run_to_position(90)
        self.dist.eyes(0,0,0,0)
        self.dist.eyes(0, 0, 100, 100)

    def run_motor(self):
        self.motor.run_for_degrees(-90)
        time.sleep(5)
        self.motor.run_for_degrees(90)
        time.sleep(5)
        self.motor.run_for_degrees(90)
        time.sleep(5)
        self.motor.run_for_degrees(-90)
        time.sleep(5)
        
if __name__ == "__main__":
    r = Cctv()
    while True:
        r.run_motor()

