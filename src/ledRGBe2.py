# ledRGBe2.py
# Practica 2. Sensores y actuadores. URJC. Diego y Ioana.

################################################################################

import time, sys
import RPi.GPIO as GPIO

################################################################################

GPIO.setmode(GPIO.BOARD)

redPin = 11
greenPin = 13
bluePin = 15

################################################################################

GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)

colors = {"red": 4, "green": 2, "blue": 1, "cyan": 3, "magenta": 5, "yellow": 6, "white": 7, "black": 0}

# Actually we are assigning numbers to each color in order to decompose them
# in a 3 bit binary number which will represent the states of the three needed
# outputs.

################################################################################

def turnOff():
   setLED("black")

def setLED(color, mode = "on"):
    rValue, gValue, bValue = bin(colors[color])[2:].zfill(3)

    rValue, gValue, bValue = bool(int(rValue)), bool(int(gValue)), bool(int(bValue))

    if color != "black":
        # Only do something if yhe color to represent is not black.
        # Actually when we turn on a color, it is substracted from the previous one.
        # That means that only the bits that match a given color are changed.
        # Same goes for the "on" mode.
        if mode == "off":
            if rValue: rValue = not rValue
            else: rValue = GPIO.input(redPin)
            if gValue: gValue = not gValue
            else: gValue = GPIO.input(greenPin)
            if bValue: bValue = not bValue
            else: bValue = GPIO.input(bluePin)

        if mode == "on":
            if rValue: pass
            else: rValue = GPIO.input(redPin)
            if gValue: pass
            else: gValue = GPIO.input(greenPin)
            if bValue: pass
            else: bValue = GPIO.input(bluePin)

    GPIO.output(redPin, rValue)
    GPIO.output(greenPin, gValue)
    GPIO.output(bluePin, bValue)
   
################################################################################

def validInput(args):
    if len(args) == 1 and args[0] == "off" or args[0] == "exit": return True
    if len(args) == 2 and args[1] in colors and (args[0] == "on" or args[0] == "off"): return True
    print("Non valid option!")
    return False # Reach this point means that the argument has not passed
    # any filter.

################################################################################

while True:
    while True:
        userCommand = input ("Enter your command! ->\t")
        if not userCommand: continue # Try again if the argument is empty.
        userCommandSplitted = userCommand.lower().split(' ')
        if validInput(userCommandSplitted): break # If the argument is valid...

    if len(userCommandSplitted) == 1:
        command = userCommandSplitted[0]
        if command == "exit": break # Break the main loop here.
        if command == "off": turnOff()
    else:
        command, color = userCommandSplitted
        if color: setLED(color, command)
    
    print("Success!")
      
turnOff()
GPIO.cleanup()

################################################################################
