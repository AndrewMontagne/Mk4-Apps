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

def redraw_home():


    ugfx.power_mode(ugfx.POWER_SLEEP)
    ugfx.clear()
    time = ugfx.Label(90, 0, 60, 16, "13:37", justification=ugfx.Label.CENTER)
    apps = get_apps()
    default_image = ugfx.Image("launcher_fancy/app.gif")

    for y in range(3):
        for x in range(3):
            i = (y * 3) + x
            root_x = 16 + (74 * x)
            root_y = 30 + (91 * y)
            ugfx.display_image(root_x, root_y, default_image)
            app_title = apps[i].title
            if app_title.len > 8:
                app_title = app_title[:7] + "..."
            ugfx.Label(root_x - 7, root_y + 60, 74, 20, app_title, justification=ugfx.Label.CENTER)

    ugfx.power_mode(ugfx.POWER_ON)

redraw_home()

while True:
    sleep.wfi()
    if Buttons.is_pressed(Buttons.BTN_Menu):
        app.restart_to_default()
