# SPDX-FileCopyrightText: Copyright (c) 2024 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_wiz`
================================================================================

CircuitPython helper library for Wiz connected lights


* Author(s): Tim Cocks

Implementation Notes
--------------------

**Hardware:**

Any CircuitPython device that supports WIFI or Ethernet networking.

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
* `Adafruit Connection Manager <https://github.com/adafruit/Adafruit_CircuitPython_ConnectionManager>`_

"""

import json
try:
    from typing import Tuple, Union
except ImportError:
    pass

import adafruit_connection_manager

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Wiz.git"

COLOR_CMD_TEMPLATE = {
    "id": 1,
    "method": "setPilot",
    "params": {"r": 0, "g": 0, "b": 0, "dimming": 75},
}
TEMPERATURE_CMD_TEMPLATE = {"id": 1, "method": "setPilot", "params": {"temp": 0, "dimming": 75}}
SCENE_CMD_TEMPLATE = {
    "id": 1,
    "method": "setPilot",
    "params": {"sceneId": 0, "dimming": 75, "speed": 175},
}
STATE_CMD_TEMPLATE = {"id": 1, "method": "setState", "params": {"state": False}}

DYNAMIC_SCENES = [
    1,
    2,
    3,
    4,
    5,
    7,
    8,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    9,
    10,
    1000,
]
SCENE_IDS = options_dict = {
    "Cozy": 6,
    "Warm White": 11,
    "Daylight": 12,
    "Cool white": 13,
    "Night light": 14,
    "Focus": 15,
    "Relax": 16,
    "True colors": 17,
    "TV time": 18,
    "Plantgrowth": 19,
    # "---Dynamic Scenes---": 0,
    "Ocean": 1,
    "Romance": 2,
    "Sunset": 3,
    "Party": 4,
    "Fireplace": 5,
    "Forest": 7,
    "Pastel Colors": 8,
    "Spring": 20,
    "Summer": 21,
    "Fall": 22,
    "Deepdive": 23,
    "Jungle": 24,
    "Mojito": 25,
    "Club": 26,
    "Christmas": 27,
    "Halloween": 28,
    "Candlelight": 29,
    "Golden white": 30,
    "Pulse": 31,
    "Steampunk": 32,
    # "---Miscellaneous---": 0,
    "Wake up": 9,
    "Bedtime": 10,
    "Rhythm": 1000,
}
"""Scene Name to Id mapping"""

MODE_RGB = 0
MODE_TEMPERATURE = 1
MODE_SCENE = 2


class WizConnectedLight:
    """
    Helper class to control Wiz connected light over WIFI via UDP.

    :param str ip: IP address of the Wiz connected light. Can be found in the smartphone app.
    :param int port: UDP port the Wiz connected light listens on. Default is 38899
    :param radio: WIFI radio object. It will attempt to use ``wifi.radio`` if not passed.
        Pass Radio objects for ESP32SPI or Wiznet ethernet networking to use them.
    :param bool debug: Enable additional debugging output.
    """

    def __init__(self, ip: str, port: int = 38899, radio=None, debug: bool = False):
        self._ip = ip
        self._port = port
        if radio is None:
            try:
                import wifi
            except ImportError:
                raise RuntimeError(
                    "Must pass radio argument during initialization for non built-in wifi."
                )
            radio = wifi.radio

        self.pool = adafruit_connection_manager.get_radio_socketpool(radio)
        self.socket = self.pool.socket(self.pool.AF_INET, self.pool.SOCK_DGRAM)
        self.socket.settimeout(3)
        self._brightness = 75
        self._speed = 125

        self.debug = debug

    @property
    def ip(self) -> str:
        """
        IP of the Wiz connected light.

        :return: The IP address of the Wiz connected light.
        """
        return self._ip

    @ip.setter
    def ip(self, new_value: str) -> None:
        self._ip = new_value

    @property
    def port(self) -> int:
        """
        UDP port the Wiz connected light listens on.

        :return: UDP port number
        """
        return self._port

    @port.setter
    def port(self, new_value: int) -> None:
        self._port = new_value

    @property
    def status(self) -> dict:
        """
        Status of the Wiz connected light.

        :return: Dictionary containing the current status of the light
        """
        data = json.dumps({"method": "getPilot", "params": {}})
        udp_message = bytes(data, "utf-8")
        self._send(udp_message)
        resp = self._recv(bufsize=400)
        resp_json = json.loads(resp)
        self._brightness = resp_json["result"]["dimming"]
        return json.loads(resp)

    def mode_from_status(self, status: dict) -> int:
        """
        Get the current mode from the status and return it.

        :param status: Light status dictionary
        :return: The mode number
        """
        if status["result"]["sceneId"] != 0:
            return MODE_SCENE
        else:
            return MODE_TEMPERATURE if "temp" in status["result"] else MODE_RGB

    @property
    def rgb_color(self) -> Tuple[int, int, int]:
        """
        RGB color of the light. Set this property to change the light to an RGB color.
        Raises an exception if accessed while not in RGB mode.

        :return: Tuple containing red, green and blue values 0-255
        """
        cur_status = self.status
        cur_mode = self.mode_from_status(cur_status)

        if cur_mode == MODE_TEMPERATURE:
            raise ValueError(
                "Light is in Temperature mode. Must change to RGB mode to read RGB color."
            )

        return (cur_status["result"]["r"], cur_status["result"]["g"], cur_status["result"]["b"])

    @rgb_color.setter
    def rgb_color(self, new_color: Tuple[int, int, int]) -> None:
        if isinstance(new_color, tuple):
            rgb_color_cmd = COLOR_CMD_TEMPLATE.copy()
            rgb_color_cmd["params"]["r"] = new_color[0]
            rgb_color_cmd["params"]["g"] = new_color[1]
            rgb_color_cmd["params"]["b"] = new_color[2]
            rgb_color_cmd["params"]["dimming"] = self._brightness
            udp_message = bytes(json.dumps(rgb_color_cmd), "utf-8")
            self._send(udp_message)
            resp = self._recv()
            if self.debug:
                print(f"UDP Response: {resp}")

    @property
    def temperature(self) -> int:
        """
        Color Temperature of the light in Kelvin. Valid values range from 2200-6200.

        :return: Color temperature value
        """
        cur_status = self.status
        cur_mode = MODE_TEMPERATURE if "temp" in cur_status["result"] else MODE_RGB
        if cur_mode == MODE_RGB:
            raise ValueError(
                "Light is in RGB mode. Must change to Temperature mode to read temperature color."
            )
        return cur_status["result"]["temp"]

    @temperature.setter
    def temperature(self, new_temperature: int) -> None:
        if new_temperature < 2200 or new_temperature > 6200:
            raise ValueError("Temperature must be between 2200 and 6200")

        temp_color_cmd = TEMPERATURE_CMD_TEMPLATE.copy()
        temp_color_cmd["params"]["temp"] = new_temperature
        temp_color_cmd["params"]["dimming"] = self._brightness

        udp_message = bytes(json.dumps(temp_color_cmd), "utf-8")
        self._send(udp_message)
        resp = self._recv()
        if self.debug:
            print(f"UDP Response: {resp}")

    @property
    def scene(self) -> int:
        """
        The SceneId of the light. Accessing the property returns
        int scene numbers. Setting the property can use the
        scene numbers or str names. See `SCENE_IDS` for valid
        scenes.

        :return: Scene number
        """
        cur_status = self.status
        return cur_status["result"]["sceneId"]

    @scene.setter
    def scene(self, new_scene: Union[int, str]) -> None:
        if isinstance(new_scene, int):
            if new_scene not in SCENE_IDS.values():
                raise ValueError(
                    "Scene ID must be a valid Scene name string, "
                    "or valid int sceneId. See SCENE_IDS dictionary."
                )

        if isinstance(new_scene, str):
            if new_scene not in SCENE_IDS.keys():
                raise ValueError(
                    "Scene ID must be a valid Scene name string, "
                    "or valid int sceneId. See SCENE_IDS dictionary."
                )
            new_scene = SCENE_IDS[new_scene]

        scene_cmd = SCENE_CMD_TEMPLATE.copy()
        scene_cmd["params"]["sceneId"] = new_scene
        scene_cmd["params"]["dimming"] = self._brightness
        scene_cmd["params"]["speed"] = self._speed
        self._send(bytes(json.dumps(scene_cmd), "utf-8"))
        resp = self._recv()
        if self.debug:
            print(f"UDP Response: {resp}")

    @property
    def brightness(self) -> int:
        """
        The brightness level of the light. Valid range is 10-100

        :return: Brightness level
        """
        return self.status["result"]["dimming"]

    @brightness.setter
    def brightness(self, new_brightness: int) -> None:
        if new_brightness < 10 or new_brightness > 100:
            raise ValueError("Brightness must be 10-100")
        cur_status = self.status
        self._brightness = new_brightness

        cur_mode = self.mode_from_status(cur_status)

        if cur_mode == MODE_RGB:
            self.rgb_color = (
                cur_status["result"]["r"],
                cur_status["result"]["g"],
                cur_status["result"]["b"],
            )
        elif cur_mode == MODE_TEMPERATURE:
            self.temperature = cur_status["result"]["temp"]
        elif cur_mode == MODE_SCENE:
            self.scene = cur_status["result"]["sceneId"]

    @property
    def speed(self) -> int:
        """
        The speed of dynamic scenes. Has no effect on static scenes.
        Valid range is 10-200.

        :return: Speed value
        """
        return self._speed

    @speed.setter
    def speed(self, new_speed: int) -> None:
        if new_speed < 10 or new_speed > 200:
            raise ValueError("Speed must be 10-200")
        cur_status = self.status
        self._speed = new_speed

        cur_mode = self.mode_from_status(cur_status)

        if cur_mode == MODE_SCENE:
            if cur_status["result"]["sceneId"] in DYNAMIC_SCENES:
                self.scene = cur_status["result"]["sceneId"]

    @property
    def state(self) -> bool:
        """
        Whether the light is on or off.

        :return: True if the light is on, False otherwise
        """
        return self.status["result"]["state"]

    @state.setter
    def state(self, new_state: bool) -> None:
        state_cmd = STATE_CMD_TEMPLATE.copy()
        state_cmd["params"]["state"] = new_state
        print(state_cmd)
        self._send(bytes(json.dumps(state_cmd), "utf-8"))
        resp = self._recv()
        if self.debug:
            print(f"UDP Response: {resp}")

    @property
    def mode(self) -> int:
        """
        The mode of the light

        :return: Mode number
        """
        return self.mode_from_status(self.status)

    def _send(self, data: bytes) -> None:
        """
        Send data on the UDP socket.

        :param data: Bytes to send
        """
        self.socket.sendto(data, (self.ip, self.port))  # send UDP packet to udp_host:port

    def _recv(self, bufsize: int = 100) -> str:
        """
        Receive data on the UDP socket.

        :param bufsize: How big of a buffer to receive into
        :return: Data received as a string
        """
        buf = bytearray(bufsize)
        try:
            self.socket.recvfrom_into(buf)
        except OSError:
            raise RuntimeError("Timeout while attempting to communicate with Wiz device")

        # print(buf)
        return buf.rstrip(b"\x00").decode("utf-8")
