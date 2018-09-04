"""Launcher for apps currently installed"""

___name___         = "Fancy Launcher"
___license___      = "MIT"
___categories___   = ["System"]
___dependencies___ = ["dialogs", "app", "sleep", "ugfx_helper"]
___launchable___   = False
___bootstrapped___ = True

import ugfx_helper, ugfx
from app import *
from dialogs import *

ugfx_helper.init()
ugfx.clear()

time = ugfx.Label(90, 0, 60, 16, "13:37", justification=ugfx.Label.CENTER)

for x in range(2):
    for y in range(2):
        root_x = 16 + (74 * x)
        root_y = 30 + (91 * y)
        ugfx.area(root_x, root_y, 60, 60, ugfx.BLACK)
        ugfx.Label(root_x, root_y + 60, 60, 16, "App", justification=ugfx.Label.CENTER)

while True:
    sleep.wfi()
