import RPi.GPIO as GPIO
import atexit
import sys
import time

pin = int(sys.argv[1])
withinRangeTimeout = int(sys.argv[2]) # In seconds
rangeThreshold = int(sys.argv[3]) # In centimeters
outOfRangeSince = None
withinRangeSince = None

print("")
print("##################################################")
print("PIN: " + str(pin))
print("RANGE THRESHOLD: " + str(rangeThreshold))
print("WITHIN RANGE TIMEOUT: " + str(withinRangeTimeout))
print("##################################################")
print("")

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
  #print(str(distance))

  return distance

def notify():
  print("NOTIFYING!!!")

#
# Run program
#
atexit.register(turnoff)

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.LOW)
delayMicroseconds(5)

while True:
  distance = measureDistance()

  print("")
  print("DISTANCE: " + str(distance))

  if (withinRangeSince is None) & (distance <= rangeThreshold):
    print("WITHIN RANGE AND WASN'T BEFORE: " + str(time.time()))
    withinRangeSince = time.time()

  if (withinRangeSince is not None) & (distance > rangeThreshold):
    print("OUT OF RANGE")
    withinRangeSince = None

  if (withinRangeSince is not None):
    secondsWithinRange = time.time() - withinRangeSince

    print("SECONDS WITHIN RANGE: " + str(secondsWithinRange))

    if secondsWithinRange > withinRangeTimeout:
      notify()

  time.sleep(1)

