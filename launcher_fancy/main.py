"""Launcher for apps currently installed"""

___name___         = "Fancy Launcher"
___license___      = "MIT"
___categories___   = ["System"]
___dependencies___ = ["dialogs", "wifi", "app", "sleep", "ugfx_helper"]
___launchable___   = False
___bootstrapped___ = False

import ugfx_helper, ugfx, buttons, wifi, time
from app import *
from dialogs import *

def redraw_home():
    ugfx.clear()

    for y in range(3):
        for x in range(3):
            i = (y * 3) + x
            root_x = 16 + (74 * x)
            root_y = 30 + (91 * y)
            ugfx.fill_circle(root_x + 30, root_y + 30, 30, ugfx.BLACK)
            ugfx.fill_circle(root_x + 30, root_y + 30, 25, ugfx.WHITE)
            app_title = apps[i].title
            if len(app_title) > 8:
                app_title = app_title[:7] + ".."
            ugfx.Label(root_x - 10, root_y + 62, 80, 20, app_title, justification=ugfx.Label.CENTER)


def draw_cursor(undraw):
    colour = ugfx.WHITE if undraw else ugfx.BLUE
    root_x = 16 + (74 * cursor_x)
    root_y = 30 + (91 * cursor_y)
    ugfx.box(root_x - 4, root_y - 4, 68, 88, colour)

def draw_wlan():
    if (wifi.is_connected()):
        strength = wifi.get_strength()
        if(strength is not None):
            wlan_label.text("%02i" % (strength))
    else:
        wlan_label.text("-")

def draw_pagination():

ugfx_helper.init()

apps = get_apps()
cursor_x = 1
cursor_y = 1
page_number = 0
page_count = len(apps) / 9
if len(apps) % 9:
    page_count += 1
wlan_label = ugfx.Label(2, 0, 60, 16, "-", justification=ugfx.Label.LEFT)

ugfx.power_mode(ugfx.POWER_SLEEP)
redraw_home()
ugfx.power_mode(ugfx.POWER_ON)
last_update = time.ticks_ms()

while True:
    sleep.sleep_ms(50)

    if buttons.is_triggered(Buttons.BTN_Menu):
        app.restart_to_default()
    if buttons.is_triggered(Buttons.BTN_B):
        redraw_home()
    if buttons.is_triggered(Buttons.BTN_1):
        apps[0].boot()
    if buttons.is_triggered(Buttons.BTN_2):
        apps[1].boot()
    if buttons.is_triggered(Buttons.BTN_3):
        apps[2].boot()
    if buttons.is_triggered(Buttons.BTN_4):
        apps[3].boot()
    if buttons.is_triggered(Buttons.BTN_5):
        apps[4].boot()
    if buttons.is_triggered(Buttons.BTN_6):
        apps[5].boot()
    if buttons.is_triggered(Buttons.BTN_7):
        apps[6].boot()
    if buttons.is_triggered(Buttons.BTN_8):
        apps[7].boot()
    if buttons.is_triggered(Buttons.BTN_9):
        apps[8].boot()
    if buttons.is_triggered(Buttons.JOY_Right) and cursor_x < 2:
        draw_cursor(True)
        cursor_x += 1
        draw_cursor(False)
    if buttons.is_triggered(Buttons.JOY_Left) and cursor_x > 0:
        draw_cursor(True)
        cursor_x -= 1
        draw_cursor(False)
    if buttons.is_triggered(Buttons.JOY_Down) and cursor_y < 2:
        draw_cursor(True)
        cursor_y += 1
        draw_cursor(False)
    if buttons.is_triggered(Buttons.JOY_Up) and cursor_y > 0:
        draw_cursor(True)
        cursor_y -= 1
        draw_cursor(False)
    if buttons.is_triggered(Buttons.JOY_Center) or buttons.is_triggered(Buttons.BTN_A):
        i = (cursor_y * 3) + cursor_x
        apps[i].boot()

    if (time.ticks_ms() - last_update > 1000):
        last_update = time.ticks_ms()
        if (!wifi.is_connected()):
            wifi.connect(wait=False, prompt_on_fail=False)
        draw_wlan()
