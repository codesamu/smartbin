from gpiozero import Servo
from time import sleep

servos = {
    "horizontal": Servo(16),
    "vertical": Servo(20)
}

def set_angle(servo, degrees):
    # limit to 0-180
    degrees = max(0, min(180, degrees))
    servo.value = (degrees / 90) - 1


while True:

    # Center both
    set_angle(servos["horizontal"], 90)
    set_angle(servos["vertical"], 90)

    side = input("Direction (l/r): ").lower()

    if side not in ["l", "r"]:
        print("Invalid input")
        continue

    vertical_angle = int(input("Vertical angle (0-180): "))

    # Horizontal left/right positions
    if side == "l":
        set_angle(servos["horizontal"], 30)
    else:
        set_angle(servos["horizontal"], 150)

    # Set custom vertical angle
    set_angle(servos["vertical"], vertical_angle)

    print("Moving...")
    sleep(2)

    print("Returning to center")

    # Move back
    set_angle(servos["vertical"], 90)
    sleep(1)

    set_angle(servos["horizontal"], 90)
    sleep(1)
