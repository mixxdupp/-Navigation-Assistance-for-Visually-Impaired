import RPi.GPIO as GPIO
from typing import Any
import time
from obstacle_avoidance.config import DISTANCE_THRESHOLD, ABSOLUTE_DISTANCE_THRESHOLD,\
    SPEED_CALCULATION_INTERVAL, SPEED_ACCEPTANCE_RANGE, SPEED_THRESHOLD
from obstacle_avoidance import warningPriorityBasedQueue

DIRECTION = ["Front", "Back", "Left", "Right"]

taskQueue = warningPriorityBasedQueue()

def measure_distance(trig_pin, echo_pin):
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(echo_pin) == 0:
        start_time = time.time()

    while GPIO.input(echo_pin) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2

    return distance

def calculate_speed_of_obstacle(trig_pin, echo_pin):
    distance1 = measure_distance(trig_pin, echo_pin)
    
    time.sleep(SPEED_CALCULATION_INTERVAL)
    
    distance2 = measure_distance(trig_pin, echo_pin)
    
    diff = distance2 - distance1
    
    speed = diff / SPEED_CALCULATION_INTERVAL
    
    return speed

async def monitor(sensor: Any, i: int) -> None:
    """
    CASES:
        1: No obstacle detected -> Just Continue
        2: An obstacle detected within the threshold
            2.1: The Speed of the obstacle -ve(meaning its moving opposite to the direction of the person) -> Just Continue
            2.2: The Speed of the obstacle +ve(meaning its moving towards the person)
                2.2.1: The distance between the person and the obstacle is increasing -> Just Continue
                2.2.2: The distance between the person and the obstacle is decreasing -> Stop and Alert the person
                
    TIME COMPLEXITY:
        Calculate distance = approx (0.001) seconds
        Get speed = approx (0.001) * 2 + 0.5 seconds
    """
    distance = sensor.get_distance()
    direction = DIRECTION[i]
    
    if distance < DISTANCE_THRESHOLD:
        speed = sensor.get_speed()
        
        if abs(speed) < SPEED_ACCEPTANCE_RANGE: # The obstacle is stationary
            pass
        elif speed < 0: # The obstacle is moving away from the person
            pass
        else: # The obstacle is moving towards the person
            if distance < ABSOLUTE_DISTANCE_THRESHOLD or speed > SPEED_THRESHOLD:
                if direction == "Front":
                    taskQueue.add(f"Moving Obstacle detected at {direction}! Watch Out!", distance, speed)
                    # Todo: Get 2 images and send to server
                else:
                    taskQueue.add(f"Moving Obstacle detected at {direction}! Watch Out!", distance, speed)
    
