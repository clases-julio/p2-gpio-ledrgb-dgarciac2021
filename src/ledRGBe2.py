# ledRGBe2.py
# Practica 2. Sensores y actuadores. URJC. Diego y Ioana.

import time, sys
import RPi.GPIO as GPIO

redPin = 11
greenPin = 13
bluePin = 15

GPIO.setmode(GPIO.BOARD)

GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)

colors = {"red": 4, "green": 2, "blue": 1, "cyan": 3, "magenta": 5, "yellow": 6, "white": 7, "black": 0}

def turnOff():
    setLED("black")

def setLED(color, mode = "on"):
    rValue, gValue, bValue = bin(colors[color])[2:].zfill(3)
    
    rValue, gValue, bValue = bool(int(rValue)), bool(int(gValue)), bool(int(bValue)) 
    
    if mode == "off":
        if rValue: rValue = not rValue
        else: rValue = GPIO.input(redPin)
        if gValue: gValue = not gValue
        else: gValue = GPIO.input(greenPin)
        if bValue: bValue = not bValue
        else: bValue = GPIO.input(bluePin)

    GPIO.output(redPin, rValue)
    GPIO.output(greenPin, gValue)
    GPIO.output(bluePin, bValue)

def validInput(args):
    if len(args) == 1 and args[0] == "off" or args[0] == "exit": return True
    if len(args) == 2 and args[1] in colors and (args[0] == "on" or args[0] == "off"): return True
    return False

while True:
    userCommandSplitted = ['']
    while not validInput(userCommandSplitted):
        userCommand = input ("Enter your command! ->\t")
        if not userCommand: continue
        userCommandSplitted = userCommand.lower().split(' ')

    if len(userCommandSplitted) == 1:
        command = userCommandSplitted[0]
        if command == "exit": break
        if command == "off": turnOff()
    else:
        command, color = userCommandSplitted
        if color: setLED(color, command)

GPIO.cleanup()

