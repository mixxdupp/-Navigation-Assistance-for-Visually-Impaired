import RPi.GPIO as GPIO
import asyncio
from obstacle_avoidance.ultrasonic_sensor import UltrasonicSensorsModule
from obstacle_avoidance import warningPriorityBasedQueue
import time
from speech.speech import Speech

GPIO.setmode(GPIO.BCM)

TRIG_PINS = [23, 24, 25, 26]
ECHO_PINS = [27, 28, 29, 30]

taskQueue = warningPriorityBasedQueue()
speech = Speech()

def monitorQueue():
    while True:
        if not taskQueue.is_empty():
            distance, speed, message = taskQueue.pop()
            speech.speak(f"Distance: {distance}, Speed: {speed}, Message: {message}")

try:
    avoidance_module = UltrasonicSensorsModule(TRIG_PINS, ECHO_PINS)
    asyncio.gather(
        avoidance_module.monitor_for_nearby_obstacles(),
        monitorQueue()
    )
except KeyboardInterrupt:
    GPIO.cleanup()
