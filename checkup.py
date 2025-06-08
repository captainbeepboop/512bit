import RPi.GPIO as GPIO
import time as time
import numpy as np
import os
import math
import subprocess

######################################### set up rows, columns and pins
rows = 8
columns = 8
switches = 8
row_pins = [18, 8, 7, 24, 15, 25, 14, 23]
#switch 7 accidentally connected to pin 28, which is not allowed
column_pins = [6, 13, 19, 26, 21, 20, 16, 12] 
switch_pins = [5, 11, 9, 10, 22, 27, 17, 4]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for x in range (columns):
    GPIO.setup(column_pins[x], GPIO.OUT)
    GPIO.output(column_pins[x], GPIO.LOW)
for x in range (rows):
    GPIO.setup(row_pins[x], GPIO.OUT)
    GPIO.output(row_pins[x], GPIO.LOW)
for x in range (switches):
    GPIO.setup(switch_pins[x], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

################### functions

def check_switches():
    count = 0
    print("------------------------------------------------------------------------INACTIVE SWITCHES:")
    for x in range (columns):
        GPIO.output(column_pins[x], GPIO.HIGH)
        for z in range(switches):
            for y in range (rows):
                GPIO.output(row_pins[y], GPIO.HIGH)
                time.sleep(0.001)

                if GPIO.input(switch_pins[z])==0:
                    print("------------------------------------------------------------------------column ", 8*x+z+1, "row ", y+1)
                    count = count + 1
                GPIO.output(row_pins[y], GPIO.LOW)
        GPIO.output(column_pins[x], GPIO.LOW)
    print("------------------------------------------------------------------------Total: ", count, " inactive switches")
######################################## the program

check_switches()
