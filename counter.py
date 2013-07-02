# imports
import time
import RPi.GPIO as GPIO
import sqlite3 as lite
import sys

# inits
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
con = lite.connect('db')

# count = 0

# endless loop, does really well at mitigating bounce
prev_input = 0
while True:
  input = GPIO.input(4)
  if ((not prev_input) and input):
    cur = con.cursor()
    cur.execute("INSERT INTO Times VALUES(" + str(time.time()) + ")")
    con.commit()
    # count += 1
    # print count
  prev_input = input
  time.sleep(.05)
