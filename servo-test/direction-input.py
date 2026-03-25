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
    for servo_name, servo in servos.items():
        servo.mid()
        sleep(0.5)

    usr_inp = input("direction (l / r & f / b) (ex. lf): ").lower()

    if usr_inp in directions:
        for servo_name, position in directions[usr_inp].items():
            getattr(servos[servo_name], position)()  # calls servo.min() / max() auf
    else:
        print("Falsche Eingabe, l/r & f/b eingeben.")
