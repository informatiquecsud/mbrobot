'''
https://github.com/informatiquecsud/mbrobot/blob/main/maqueen-lite/pyodide-robotsim/microbit.py
'''

from js import window, document
from pyodide import to_js
import os

# Detect platform
_platform = None
if os.uname().sysname == 'Emscripten':
    _platform = 'pyodide'
elif os.uname().sysname == 'microbit':
    _platform = 'microbit'


class Pin:
    def __init__(self, pin):
        self._pin = pin
    
    
pin19 = Pin(19)
pin20 = Pin(20)


class I2C:
    
    def __init__(self):
        pass
    
    def _set_i2c_device(self, device):
        self._i2c_device = device
    
    def init(self, freq=100000, sda=pin20, scl=pin19):
        pass
    
    def scan(self):
        return [0x10]
    
    def read(self, addr, n, repeat=False):
        return self._i2c_device.write(addr, n)
    
    def write(self, addr, buf, repeat=False):
        return self._i2c_device.write(addr, to_js(buf))
    
    
if _platform == 'pyodide':
    iframe = document.querySelector('iframe.robotsim-container')
    sim = iframe.contentWindow.sim
    bot_i2c = sim.robots[0].i2c
    i2c = I2C()
    i2c._set_i2c_device(bot_i2c)

    pin13 = sim.robots[0].pin13
    pin14 = sim.robots[0].pin14
    pin8 = sim.robots[0].pin8
    pin12 = sim.robots[0].pin12

