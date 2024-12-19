# SPDX-FileCopyrightText: Copyright (c) 2024 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Basic demonstration of Wiz light control using 4 push buttons each
wired to their own pin.
"""

import time

import board
import wifi
from digitalio import DigitalInOut, Direction, Pull

from adafruit_wiz import SCENE_IDS, WizConnectedLight

udp_host = "192.168.1.143"  # IP of UDP Wiz connected light
udp_port = 38899  # Default port is 38899, change if your light is configured differently

my_lamp = WizConnectedLight(udp_host, udp_port, wifi.radio, debug=True)

# Basic push buttons initialization
btn_1 = DigitalInOut(board.D11)
btn_1.direction = Direction.INPUT
btn_1.pull = Pull.UP

btn_2 = DigitalInOut(board.D12)
btn_2.direction = Direction.INPUT
btn_2.pull = Pull.UP

btn_3 = DigitalInOut(board.A1)
btn_3.direction = Direction.INPUT
btn_3.pull = Pull.UP

btn_4 = DigitalInOut(board.A0)
btn_4.direction = Direction.INPUT
btn_4.pull = Pull.UP

# list of colors to cycle through
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
# current index in the color cycle
cur_rgb_index = 0

# list of temperatures to cycle through
temperatures = [2200, 2800, 3600, 4800, 6200]
# current index in the temperature cycle
cur_temp_index = 0

while True:
    # if btn 1 pressed
    if not btn_1.value:
        print("Button 1")
        # toggle the on/off state
        my_lamp.state = not my_lamp.state
        time.sleep(0.5)

    # if btn 2 pressed
    if not btn_2.value:
        print("Button 2")
        # set the current RGB color
        my_lamp.rgb_color = colors[cur_rgb_index]
        # increment the index for next time and wrap around to zero as needed
        cur_rgb_index = (cur_rgb_index + 1) % len(colors)
        time.sleep(0.5)

    # if btn 3 pressed
    if not btn_3.value:
        print("Button 3")
        # set the current light color temperature
        my_lamp.temperature = temperatures[cur_temp_index]
        # increment the index for next time and wrap around to zero as needed
        cur_temp_index = (cur_temp_index + 1) % len(temperatures)
        time.sleep(0.5)

    # if btn 4 pressed
    if not btn_4.value:
        print("Button 4")
        # uncomment to see the available scenes
        # print(SCENE_IDS.keys())

        # set the scene
        my_lamp.scene = "Party"
        time.sleep(0.5)
