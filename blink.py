import RPi.GPIO as GPIO
import time
import atexit

def turnoff():
  GPIO.output(18, GPIO.LOW)

def turnon():
  GPIO.output(18, GPIO.HIGH)

atexit.register(turnoff) # Ensures we shut light off on program exit
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

while True:
  turnon()
  time.sleep(1)
  turnoff()
  time.sleep(1)

