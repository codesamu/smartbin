from gpiozero import Servo
from time import sleep

servo = Servo(20)

while True:
    servo.mid()
    sleep(2)
#    servo.max()
    sleep(2)
