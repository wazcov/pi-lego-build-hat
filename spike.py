import signal
from buildhat import Motor, MotorPair, DistanceSensor
import time
import threading

radar = Motor('A')

dist = DistanceSensor('B', threshold_distance=1000)

wheels = MotorPair('C', 'D')
rwheel = Motor('C')
lwheel = Motor('D')

def handle_motor(speed, pos, apos):
    print("Motor", speed, pos, apos)
    
def run_radar(radar):
    radar.run_for_rotations(100)

def right(wheels):
    wheels.run_for_rotations(1, directionr=-1, directionl=-1)
    
def left(wheels):
    wheels.run_for_rotations(1)
    
def forward(wheels):
    wheels.run_for_rotations(2, directionr=-1)
    
def handle_in(distance):
    print("in range", distance)
    radar.start()

def handle_out(distance):
    print("out of range", distance)
    radar.stop()
    
dist.when_in_range = handle_in
dist.when_out_of_range = handle_out
    
def reverse(wheels):
    wheels.run_for_rotations(2, directionl=-1)
    
def drive_pattern(wheels, radar):
    forward(wheels)
    right(wheels)   
    forward(wheels)
    
    time.sleep(3)
    reverse(wheels)
    left(wheels)
    reverse(wheels)
    
    time.sleep(3)
    forward(wheels)
    left(wheels)   
    forward(wheels)
    
    time.sleep(3)
    reverse(wheels)
    right(wheels)
    reverse(wheels)
        
    radar.stop()
    wheels.stop()
        

def run_app():
    print("Starting...")

    radar.set_default_speed(25)
    lwheel.set_default_speed(50)
    rwheel.set_default_speed(50)
    wheels.set_default_speed(50)
    
#     radarthread = threading.Thread(target=run_radar, name="Radar", args=[radar])
#     radarthread.start()
    
    drive_pattern(wheels, radar)


try:
    run_app()
        
except Exception as e:
    print(e)

