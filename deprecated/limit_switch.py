import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)

pushpin = 2 # set input push button pin
GPIO.setup(pushpin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # with pull up resistor

while True:
    print(GPIO.input(pushpin))
    sleep(0.2)