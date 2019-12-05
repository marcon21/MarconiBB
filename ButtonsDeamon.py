import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True: # Run forever
    if GPIO.input(10) == GPIO.HIGH:
        print("Button was pushed!")