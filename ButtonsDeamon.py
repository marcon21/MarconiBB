import RPi.GPIO as GPIO
import requests

#PIN BOTTONI
BUTTON_1 = 22
BUTTON_2 = 24
BUTTON_3 = 26

def button1Pressed(channel):
    print("Tasto 1 premuto")

    if GPIO.input(BUTTON_1) == GPIO.HIGH:
        print(requests.get('http://localhost:5000/button1'))

def button2Pressed(channel):
    print("Tasto 2 premuto")

    if GPIO.input(BUTTON_2) == GPIO.HIGH:
        print(requests.get('http://localhost:5000/button2'))

def button3Pressed(channel):
    print("Tasto 3 premuto")

    if GPIO.input(BUTTON_3) == GPIO.HIGH:
        print(requests.get('http://localhost:5000/button3'))

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUTTON_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(BUTTON_1, GPIO.RISING, callback=button1Pressed)
GPIO.add_event_detect(BUTTON_2, GPIO.RISING, callback=button2Pressed)
GPIO.add_event_detect(BUTTON_3, GPIO.RISING, callback=button3Pressed)

while True:
    pass
