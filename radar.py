from signal import pause
from buildhat import Motor, DistanceSensor

class Radar:
    radar = Motor('A')
    radar.set_default_speed(25)
    dist = DistanceSensor('B', threshold_distance=300)
    
    def __init__(self):
        self.dist.eyes(0,0,0,0)
        # self.dist.eyes(100, 100, 100, 100)
        self.dist.when_in_range = self.handle_in
        self.dist.when_out_of_range = self.handle_out

    def handle_in(self, distance):
        print("in range", distance)
        self.dist.eyes(10, 10, 100, 100)
        self.radar.start()

    def handle_out(self, distance):
        print("out of range", distance)
        self.dist.eyes(100, 100, 100, 100)
        self.radar.stop()
        
if __name__ == "__main__":
    r = Radar()
    pause()

