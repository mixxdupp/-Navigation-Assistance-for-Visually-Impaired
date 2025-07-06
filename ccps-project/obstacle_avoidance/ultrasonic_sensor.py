import RPi.GPIO as GPIO
import asyncio
from typing import List
import time
from obstacle_avoidance.utils import measure_distance,\
    calculate_speed_of_obstacle, monitor

class UltrasonicSensor:
    trig_pin = None
    echo_pin = None
    
    def __init__(self, trig_pin: int, echo_pin: int) -> None:
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
    def get_distance(self):
        return measure_distance(self.trig_pin, self.echo_pin)
    
    def get_speed(self):
        return calculate_speed_of_obstacle(self.trig_pin, self.echo_pin)
    
    def __del__(self):
        GPIO.cleanup(self.trig_pin)
        GPIO.cleanup(self.echo_pin)

class UltrasonicSensorsModule:
    front_sensor = None
    back_sensor = None
    left_sensor = None
    right_sensor = None
    
    def __init__(self, trig_pins: List[int], echo_pins: List[int]) -> None:
        self.front_sensor = UltrasonicSensor(trig_pins[0], echo_pins[0])
        self.back_sensor = UltrasonicSensor(trig_pins[1], echo_pins[1])
        self.left_sensor = UltrasonicSensor(trig_pins[2], echo_pins[2])
        self.right_sensor = UltrasonicSensor(trig_pins[3], echo_pins[3])
        
    async def monitor_for_nearby_obstacles(self):
        while True:
            await asyncio.gather(
                monitor(self.front_sensor, 0),
                monitor(self.back_sensor, 1),
                monitor(self.left_sensor, 2),
                monitor(self.right_sensor, 3)
            )
            time.sleep(1)