from gpiozero import Servo
from time import sleep

servo = Servo(20)

def set_angle(degrees):
    # convert 0-180 degrees to -1 to +1
    servo.value = (degrees / 90) - 1
    print("sleeping")
    sleep(2)

while True:
    usr_input=int(input("degree: "))
    set_angle(usr_input)


