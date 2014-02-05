import RPi.GPIO as GPIO
import atexit
import sys
import time
from twilio.rest import TwilioRestClient

import logging
logger = logging.getLogger('inhaler')
hdlr = logging.FileHandler('/var/log/inhaler.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)
logger.debug("\n***********************************")
logger.debug("APP STARTED AT")
logger.debug("***********************************\n")

pin = int(sys.argv[1])
withinRangeTimeout = int(sys.argv[2]) # In seconds
rangeThreshold = int(sys.argv[3]) # In centimeters
notificationTimeout = int(sys.argv[4]) # In seconds
distanceCheckInterval = int(sys.argv[5])
outOfRangeSince = None
withinRangeSince = None
lastNotifiedAt = time.time() - notificationTimeout

logger.debug("")
logger.debug("##################################################")
logger.debug("PIN: " + str(pin))
logger.debug("RANGE THRESHOLD: " + str(rangeThreshold))
logger.debug("WITHIN RANGE TIMEOUT: " + str(withinRangeTimeout))
logger.debug("NOTIFICATION TIMEOUT: " + str(notificationTimeout))
logger.debug("##################################################")
logger.debug("")

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

  #logger.debug("ELAPSED TIME: " + str(elapsed))
  #logger.debug("DISTANCE: " + str(distance))
  #logger.debug(str(distance))

  return distance

def notify():
  # TODO: Make system call to Twilio!!!
  logger.debug("\n\n**************************")
  logger.debug("NOTIFYING!!!")
  logger.debug("**************************\n")

  ACCOUNT_SID = "AC1cbd1a59c8e0d958a72fbdbfd22f443a"
  AUTH_TOKEN = "5e70041ab8f9532d5b60691b8dae0aa0"

  client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

  client.messages.create(
    to="6128591572",
    from_="+16122550964",
    body="TIme for Pastor's inhaler!",
  )

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

  logger.debug("")
  logger.debug("DISTANCE: " + str(distance))

  # Object is within range for first time
  if (withinRangeSince is None) and (distance <= rangeThreshold):
    logger.debug("WITHIN RANGE AND WASN'T BEFORE: " + str(time.time()))
    withinRangeSince = time.time()

  # Object is now out of range
  if (withinRangeSince is not None) and (distance > rangeThreshold):
    logger.debug("OUT OF RANGE")
    withinRangeSince = None

  # Determine how long the object has been within range and if notifications should be sent
  if (withinRangeSince is not None):
    secondsWithinRange = time.time() - withinRangeSince

    logger.debug("SECONDS WITHIN RANGE: " + str(secondsWithinRange))

    if secondsWithinRange > withinRangeTimeout:
      # OLD
      #if (lastNotifiedAt is None):
        #notify()
        #lastNotifiedAt = time.time()
      #else:
      #  secondsSinceLastNotification = (time.time() - lastNotifiedAt)
      #  logger.debug("SECONDS SINCE LAST NOTICE: " + str(secondsSinceLastNotification))

      #  if (secondsSinceLastNotification > notificationTimeout):
      #    notify()
      #    lastNotifiedAt = time.time()

      # NEW
      secondsSinceLastNotification = (time.time() - lastNotifiedAt)
      logger.debug("SECONDS SINCE LAST NOTICE: " + str(secondsSinceLastNotification))

      if (secondsSinceLastNotification > notificationTimeout):
        notify()
        lastNotifiedAt = time.time()

  time.sleep(distanceCheckInterval)

