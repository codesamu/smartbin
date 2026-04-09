from gpiozero import Servo
from time import sleep

servos = {
    "horizontal": Servo(16),
    "vertical": Servo(20)
}

directions = {
    "lf": {"horizontal": "min", "vertical": "min"},
    "rf": {"horizontal": "max", "vertical": "min"},
    "lb": {"horizontal": "min", "vertical": "max"},
    "rb": {"horizontal": "max", "vertical": "max"},
}

while True:
    for dir_name, positions in directions.items():
        print(f"Bewege Servos nach: {dir_name}")
        for servo_name, position in positions.items():
            getattr(servos[servo_name], position)()  # servo.min() or servo.max()
            sleep(2)
        print('going initial position')
        for servo in servos.values():
            servo.mid()
            print('centering between')
            sleep(1)
        sleep(3)  

    # go to inital middle position between positions
    for servo in servos.values():
        servo.mid()
    print('waiting for centering')
    sleep(1.5)
