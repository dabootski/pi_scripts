import RPi.GPIO as GPIO
import atexit
import sys
import time

pin = int(sys.argv[1])

def delayMicroseconds(num):
  time.sleep(num/1000000.0)

def turnoff():
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, GPIO.LOW)

def measureDistance():
  # Emit quick pulse
  GPIO.output(pin, GPIO.HIGH)
  delayMicroseconds(10)
  GPIO.output(pin, GPIO.LOW)

  # Change pin to input and measure pulse width
  GPIO.setup(pin, GPIO.IN)

  start = time.time()
  stop = time.time()

  while GPIO.input(pin) == 0:
    start = time.time()

  while GPIO.input(pin) == 1:
    stop = time.time()

  GPIO.setup(pin, GPIO.OUT)

  elapsed = stop - start

  # Distance pulse travelled in that time is time
  # multiplied by the speed of sound (cm/s)
  distance = elapsed * 34000

  # That was the distance there and back so halve the value
  distance = distance / 2

  #print("ELAPSED TIME: " + str(elapsed))
  #print("DISTANCE: " + str(distance))
  print(str(distance))

  distance

#
# Run program
#
atexit.register(turnoff)

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.LOW)
delayMicroseconds(5)

while True:
  measureDistance()
  time.sleep(1)

