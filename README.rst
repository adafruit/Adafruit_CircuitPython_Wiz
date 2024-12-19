Introduction
============


.. image:: https://readthedocs.org/projects/adafruit-circuitpython-wiz/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/wiz/en/latest/
    :alt: Documentation Status


.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/adafruit/Adafruit_CircuitPython_Wiz/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_Wiz/actions
    :alt: Build Status


.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff

CircuitPython helper library for Wiz connected lights.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.



Works with any CircuitPython device has built-in WIFI.

`Purchase one from the Adafruit shop <http://www.adafruit.com/products/>`_

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-wiz/>`_.
To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-wiz

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-wiz

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .env/bin/activate
    pip3 install adafruit-circuitpython-wiz

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install adafruit_wiz

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: python

    import wifi

    from adafruit_wiz import SCENE_IDS, WizConnectedLight

    udp_host = "192.168.1.143"  # IP of UDP Wiz connected light
    udp_port = 38899  # Default port is 38899, change if your light is configured differently

    my_lamp = WizConnectedLight(udp_host, udp_port, wifi.radio)

    print(f"Current Status: {my_lamp.status}")

    # set RGB Color
    my_lamp.rgb_color = (255, 0, 255)

    # set light color temperature
    # my_lamp.temperature = 4400

    # print available scenes
    # print(SCENE_IDS.keys())

    # set the scene
    # my_lamp.scene = "Party"


Documentation
=============
API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/wiz/en/latest/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_Wiz/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
