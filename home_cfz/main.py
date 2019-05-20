"""Default homescreen

This is the default homescreen for the Tilda Mk4.
It gets automatically installed when a badge is
newly activated or reset.
"""

___title___        = "ConFuzzled Home"
___license___      = "MIT"
___categories___   = ["Homescreens"]
___dependencies___ = ["homescreen", "shared/logo.png", "shared/sponsors.png"]
___launchable___   = False
___bootstrapped___ = True

import ugfx
from homescreen import *
import machine, math, sleep

init()

def get_backlight_brightness():
    return max(min(tilda.Sensors.get_lux(), 99), 1)

def set_backlight(level):
    machine.PWM(machine.PWM.PWM_LCDBL).duty(math.floor(level))

def image_transition(image):
    for i in range(0, 20):
        set_backlight(average_backlight * (1.0 - (i / 20.0)))
        sleep.sleep(0.05)

    set_backlight(0)
    ugfx.display_image(0, 0, "home_cfz/image" + str(image) + ".png")

    for i in range(0, 20):
        set_backlight(average_backlight * (i / 20.0))
        sleep.sleep(0.05)

    set_backlight(average_backlight)

average_backlight = get_backlight_brightness()
num_images = 12
current_image = 1
counter = 0

# update loop
while True:
    average_backlight = ((average_backlight * 9) + get_backlight_brightness()) / 10
    set_backlight(average_backlight)
    sleep_or_exit(0.5)

    counter += 1

    if counter > 10:
        current_image += 1
        counter = 0
        if current_image > num_images:
            current_image = 1
        image_transition(current_image)
