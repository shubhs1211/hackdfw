import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin
while True:
    i=GPIO.input(11)
    if i==0:                 #When output from motion sensor is LOW
        print "No intruders",i
    else:
        print "Intruder alert"
    time.sleep(0.2)
