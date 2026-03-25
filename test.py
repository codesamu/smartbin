from gpiozero import Servo
from time import sleep

servos = [Servo(16), Servo(20)]  # GPIO16 und GPIO20

positions = ['min', 'mid', 'max']

while True:
    for servo in servos:
        for pos in positions:
            getattr(servo, pos)()  
            sleep(1)
