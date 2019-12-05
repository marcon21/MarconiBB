import RPi.GPIO as GPIO

#PIN BOTTONI:

BOTTONE_1 = 22
BOTTONE_2 = 24
BOTTONE_3 = 26

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BOTTONE_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BOTTONE_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BOTTONE_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(BOTTONE_1, GPIO.RISING, callback=buttonPressed)
GPIO.add_event_detect(BOTTONE_2, GPIO.RISING, callback=buttonPressed)
GPIO.add_event_detect(BOTTONE_3, GPIO.RISING, callback=buttonPressed)
