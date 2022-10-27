# P2-gpio-ledrgb

This exercise consists on drive a [RGB LED](https://github.com/clases-julio/p2-gpio-ledrgb-dgarciac2021/wiki/RGB-LED) with the [GPIO](https://github.com/clases-julio/p1-introrpi-pwm-dgarciac2021/wiki/GPIO) available on the [Raspberry Pi 3B+](https://github.com/clases-julio/p1-introrpi-pwm-dgarciac2021/wiki/Raspberry-Pi#raspberry-pi-3b). You might want to take a look on the [wiki](https://github.com/clases-julio/p2-gpio-ledrgb-dgarciac2021/wiki), since there is info of everything involved on this project. From the [RGB color model](https://github.com/clases-julio/p2-gpio-ledrgb-dgarciac2021/wiki/RGB) to the [RGB LED](https://github.com/clases-julio/p2-gpio-ledrgb-dgarciac2021/wiki/RGB-LED).

## Circuit Assembly

The assembly is pretty straight-forward, just like [the previous one](https://github.com/clases-julio/p1-introrpi-pwm-dgarciac2021) but repeated three times. However, this time we are using a fixed value of Ω for each color (47Ω for **R**ed and 10Ω for **G**reen and **B**lue)[^1]

This is an schematic made with [Fritzing](https://fritzing.org/):

![Schematic](./.img/schematic.png)

And this is the real circuit!

![Aerial view](./.img/aerial-view.jpg)

## Code

We would like yo highlight some remarkable aspects from our code.

### Dictionary

We decided to go for this data type to store the available colors since the key (*A.K.A.* the color) is being provided exactly by the user. This way we can easily extract the assigned value for each color directly from the user input, along with some security checks (Like for example, if the color really exists)

```python
colors = {"red": 4, "green": 2, "blue": 1, "cyan": 3, "magenta": 5, "yellow": 6, "white": 7, "black": 0}
```

Actually this numbers are intended to be decomposed in its binary representation. Each bit will represent a value for the output of each LED.

|Color|Deciamal|Binary (RGB)|
|---|---|---|
|Red|4|1 0 0|
|Green|2|0 1 0|
|Blue|1|0 0 1|
|...|...|...|

### Not all bits

Instead of rewrite the new color over the last color, we made a different implementation.

When the user enters any command followed by a color, this color will be added or substracted to the current color showed on the led. This translates to only the involved bits are changed and the rest remain in its previous state. 

```python
        # Only do something if the color to represent is not black.
        # Actually when we turn on a color, it is substracted from the previous one.
        # That means that only the bits that match a given color are changed.
        # Same goes for the "on" mode.
        if mode == "off": # Turn off a color means flip its bits!
            if rValue: rValue = not rValue
            else: rValue = GPIO.input(redPin)
            if gValue: gValue = not gValue
            else: gValue = GPIO.input(greenPin)
            if bValue: bValue = not bValue
            else: bValue = GPIO.input(bluePin)

        if mode == "on": # pass = do nothing. This is used since the if statment could not be empty.
            if rValue: pass 
            else: rValue = GPIO.input(redPin)
            if gValue: pass
            else: gValue = GPIO.input(greenPin)
            if bValue: pass
            else: bValue = GPIO.input(bluePin)
```

With this aproach we achieve a particular behaviour. For example, if the LED is already turned on in red and the user enters `on blue`, this two colors will be added giving a final magenta color. The substraction just works the same but in the opposite direction. Of course, you can do this with any given color, included those which are composed like cyan, yellow... even white which is a mix of all of them!

### Is valid?

With this snippet we want to point out the usage of multipe `return` statments. However, **only one of them will actually execute**.

```python
def validInput(args):
    if len(args) == 1 and args[0] == "off" or args[0] == "exit": return True
    if len(args) == 2 and args[1] in colors and (args[0] == "on" or args[0] == "off"): return True
    print("Non valid option!")
    return False # Reach this point means that the argument has not passed
    # any filter.
```

The argument will be *filtered* according to a given parameters.[^2] Once any filter is passed, the method returns `True`. Reaching the bottom of the method will mean that none filter has passed so the argument will be considered as a non valid option, thus returns `False`. This method is used as a test condition to break the loop where the program ask the user to enter a command.

```python
while True:
        userCommand = input ("Enter your command! ->\t")
        if not userCommand: continue # Try again if the argument is empty.
        userCommandSplitted = userCommand.lower().split(' ')
        if validInput(userCommandSplitted): break # If the argument is valid...
```

## Circuit testing

This is the result! Pretty nice, isn't it?

![Schematic](./.img/better-colors.gif)

[^1]: Those resistor values were calculated for approximately 16mA of current for each channel. This resulted to be too bright (Both for our eyes and for the camera) so in the real circuit **two** leds are used simultaneously in order to half that current between and therefore make them dimmer.
[^2]: Worth to mention also the order of the conditions given, seeking optimization.
