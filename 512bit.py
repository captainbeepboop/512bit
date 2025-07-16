import RPi.GPIO as GPIO
import time as time
import numpy as np
import os
import math
import subprocess
from random import randrange

######################################### disable cursor
os.system('tput civis')

######################################### timing
last_update = 0

######################################### set up rows, columns and pins
rows = 8
columns = 8
switches = 8
row_pins = [18, 8, 7, 24, 15, 25, 14, 23]
#switch 7 accidentally connected to pin 28, which is not allowed
column_pins = [6, 13, 19, 26, 21, 20, 16, 12] 
switch_pins = [5, 11, 9, 10, 22, 27, 17, 4]

colours = [0]*(rows*columns)
 
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

########################################## set up screen buffer

fbset_string = subprocess.check_output("fbset", shell=True, text=True)
fbset_values = [int(s) for s in fbset_string.split() if s.isdigit()]

screen_width = fbset_values[2]
screen_height = fbset_values[3]
pixel_width = screen_height//8
pixel_offset = (screen_width - pixel_width*8)//2

#set up frame buffer
buf = np.memmap('/dev/fb0', dtype='uint16',mode='w+', shape=(screen_height,screen_width))

start_time = time.time()

########################################## functions

def byte_to_16(colour_8_bit):
    red = colour_8_bit >> 5
    green = (colour_8_bit & 0b11100) >> 2
    blue = colour_8_bit & 0b11 
    red = (red*31)//7
    green = (green*63)//7
    blue = (blue*31)//3
    result = (red << 11) + (green << 5) + blue
    return result

def draw_pixel(pixel, colour_8_bit):
    colour_16_bit = byte_to_16(colour_8_bit)
    r = pixel // 8
    c = pixel % 8
    buf[r*pixel_width:r*pixel_width+pixel_width,c*pixel_width+pixel_offset:c*pixel_width+pixel_width+pixel_offset] = colour_16_bit
   
def clear_screen():
    buf[:] = 0

def update_history(pixel):
    current_time = str(math.floor(1000*(time.time() - start_time)))
    with open("/home/cris-edwards/Desktop/history.txt", 'a') as file:
            file.write(current_time+" - "+str(pixel)+" - "+str(colours[pixel])+"\n")        

def start_history():
    with open("/home/cris-edwards/Desktop/history.txt", 'a') as file:
            file.write(time.strftime('%x %X')+"\n")
            for i in range (64):
                file.write(str(colours[i])+"-")
            file.write("\n")
             
            
def check_time():
    global last_update
    current_time = math.floor(time.time())
    if current_time > last_update and current_time % 255 == 0:
        update_website()
        last_update = current_time

def check_switches():
    for x in range (columns):
        GPIO.output(column_pins[x], GPIO.HIGH)
        for y in range (rows):
            GPIO.output(row_pins[y], GPIO.HIGH)
            time.sleep(0.001)
            for z in range (switches):
                current_colour = colours[y*columns + x]
                if GPIO.input(switch_pins[z]):
                    current_colour |= (1<<(7-z))
                else:
                    current_colour &=~ (1<<(7-z))
                pixel = y*columns + x
                if current_colour != colours[pixel]:
                    colours[pixel] = current_colour
                    draw_pixel(pixel, current_colour)
                    if startup == 0:
                        update_history(pixel)
            GPIO.output(row_pins[y], GPIO.LOW)
        GPIO.output(column_pins[x], GPIO.LOW)
     

######################################## the program

clear_screen()
startup = 1
check_switches()
start_history()
startup = 0

try:
    while True:
        check_switches()
except KeyboardInterrupt:
    clear_screen()
    pass
