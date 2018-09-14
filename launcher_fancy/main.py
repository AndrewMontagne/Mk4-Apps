"""Launcher for apps currently installed"""

___title___        = "Fancy Launcher"
___license___      = "MIT"
___categories___   = ["System"]
___dependencies___ = ["dialogs", "wifi", "app", "sleep"]
___launchable___   = False
___bootstrapped___ = False

import ugfx
import ugfx_helper
import buttons
import time
import sim800
from tilda import Sensors
from app import *
from dialogs import *
ugfx_helper.init()

background_default = ugfx.html_color(0x800080)
background_selected = ugfx.WHITE
foreground_default = ugfx.WHITE
foreground_selected = ugfx.html_color(0x800080)
fifty_percent_colour = ugfx.html_color(0xbf80bf)

default_style = ugfx.Style()
default_style.set_enabled([foreground_default, foreground_default, background_default, background_default])
default_style.set_focus(foreground_default)
default_style.set_background(background_default)

selected_style = ugfx.Style()
selected_style.set_enabled([foreground_selected, foreground_selected, background_selected, background_selected])
selected_style.set_focus(foreground_selected)
selected_style.set_background(background_selected)

ugfx.set_default_style(default_style)

average_charge = 0
apps = get_apps()
cursor_x = 1
cursor_y = 1
labels = [None] * 9


def draw_app(x, y, selected=False, update_background=False):
    background = background_selected if selected else background_default
    foreground = foreground_selected if selected else foreground_default
    style = selected_style if selected else default_style

    root_x = 16 + (74 * x)
    root_y = 30 + (91 * y)
    i = (y * 3) + x

    if update_background or selected:
        ugfx.area(root_x - 4, root_y - 4, 68, 82, background)

    ugfx.fill_circle(root_x + 30, root_y + 30, 30, foreground)
    ugfx.fill_circle(root_x + 30, root_y + 30, 25, background)
    app_title = apps[i].title

    if update_background and labels[i] is not None:
        labels[i].destroy()
        labels[i] = None

    if labels[i] is None:
        labels[i] = ugfx.Label(root_x - 4, root_y + 62, 68, 20, app_title, style=style, justification=ugfx.Label.CENTERTOP)
    else:
        labels[i].text(app_title)


def redraw_home():
    ugfx.clear(background_default)

    for y in range(3):
        for x in range(3):
            draw_app(x, y, cursor_y == y and cursor_x == x)

    draw_battery(True)
    draw_carrier(True)
    draw_clock(True)
    draw_pager(True)


def draw_carrier(force=False):
    rssi = sim800.rssi()
    carrier = sim800.currentoperator()
    if len(carrier) == 0:
        text = "No Service"
    else:
        text = "%02i %s" % (rssi, carrier)

    if carrier_label.text() != text or force:
        carrier_label.text(text)


def draw_clock(force=False):
    rtc = machine.RTC()

    # Set time with SIM800
    if rtc.now()[0] < 2018 and carrier_label.text() != "No Service":
        if(sim800.command("AT+CLTS?")[1] != "+CLTS: 1"): # Not set to get time
            sim800.command("AT+CLTS=1") # Enable time fetch
            sim800.command("AT+AT&W") # Save setting
            sim800.command("AT+COPS=2") # Disconnect
            sim800.command("AT+COPS=0") # Reconnect

        time = sim800.command("AT+CCLK?")[1][8:-4]
        if len(time) != 17:
            return

        year = 2000 + int(time[0:2])
        month = int(time[3:5])
        day = int(time[6:8])
        hour = int(time[9:11])
        min = int(time[12:14])
        sec = int(time[15:17])
        rtc.init((year, month, day, hour, min, sec))

    now = rtc.now()[:6]
    hour = now[3]
    minute = now[4]

    if now[0] < 2018:
        text = "%02i:%02i" % (hour, minute)
    else:
        text = ""

    if clock_label.text() != text or force:
        clock_label.text(text)


def draw_battery(force=False):
    global average_charge
    if average_charge == 0:
        average_charge = sim800.batterycharge()
    else:
        average_charge = ((average_charge * 4) + sim800.batterycharge()) / 5

    if Sensors.get_charge_status() == Sensors.BAT_NOT_CHARGING:
        text = "%02i%%" % average_charge
    else:
        text = "+%02i%%" % average_charge

    if battery_label.text() != text or force:
        battery_label.text(text)


def handle_select(new_x, new_y):
    global cursor_x, cursor_y
    if new_x == cursor_x and new_y == cursor_y:
        i = (cursor_y * 3) + cursor_x
        return apps[i].boot()

    draw_app(cursor_x, cursor_y, False, True)
    cursor_x = new_x
    cursor_y = new_y
    draw_app(cursor_x, cursor_y, True, True)


def draw_pager(force=False):
    ugfx.area(screen_centre + (-4 - 8), 302, 8, 8, ugfx.WHITE)
    ugfx.area(screen_centre + (-4 + 8), 302, 8, 8, ugfx.html_color(0xbf80bf))


page_number = 0
page_count = len(apps) / 9
if len(apps) % 9:
    page_count += 1

screen_centre = int((ugfx.width() / 2))

carrier_label = ugfx.Label(2, 0, 98, 16, "", justification=ugfx.Label.LEFTTOP)
clock_label = ugfx.Label(screen_centre - 30, 0, 60, 16, "", justification=ugfx.Label.CENTERTOP)
battery_label = ugfx.Label(ugfx.width() - 82, 0, 80, 16, "", justification=ugfx.Label.RIGHTTOP)

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
        handle_select(0, 0)
    if buttons.is_triggered(Buttons.BTN_2):
        handle_select(1, 0)
    if buttons.is_triggered(Buttons.BTN_3):
        handle_select(2, 0)
    if buttons.is_triggered(Buttons.BTN_4):
        handle_select(0, 1)
    if buttons.is_triggered(Buttons.BTN_5):
        handle_select(1, 1)
    if buttons.is_triggered(Buttons.BTN_6):
        handle_select(2, 1)
    if buttons.is_triggered(Buttons.BTN_7):
        handle_select(0, 2)
    if buttons.is_triggered(Buttons.BTN_8):
        handle_select(1, 2)
    if buttons.is_triggered(Buttons.BTN_9):
        handle_select(2, 2)
    if buttons.is_triggered(Buttons.JOY_Right) and cursor_x < 2:
        handle_select(cursor_x + 1, cursor_y)
    if buttons.is_triggered(Buttons.JOY_Left) and cursor_x > 0:
        handle_select(cursor_x - 1, cursor_y)
    if buttons.is_triggered(Buttons.JOY_Down) and cursor_y < 2:
        handle_select(cursor_x, cursor_y + 1)
    if buttons.is_triggered(Buttons.JOY_Up) and cursor_y > 0:
        handle_select(cursor_x, cursor_y - 1)
    if buttons.is_triggered(Buttons.JOY_Center) or buttons.is_triggered(Buttons.BTN_A):
        handle_select(cursor_x, cursor_y)

    if time.ticks_ms() - last_update > 5000:
        last_update = time.ticks_ms()
        draw_battery()
        draw_carrier()
        draw_clock()
