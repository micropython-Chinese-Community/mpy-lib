# mpy-lib
# SHT3x humidity and temperature sensor 8bit I2C micropython drive
# ver: 1.0
# License: MIT
# Author: shaoziyang
# https://github.com/micropython-Chinese-Community/mpy-lib

from time import sleep_ms

class SHT3x():

    def __init__(self, i2c, addr = 68):
        self.i2c = i2c
        self._addr = addr
        self.ver = '1.0'
        self.info = 'SHT3x I2C drive for micropython'
        self._mode = 1
        self._cmd = 0x240b
        self._delay = 6
        self._decimal = 1
        self._tb = bytearray(2)
        self._rb = bytearray(3)
        self._ht = bytearray(6)
        self._T = 0
        self._H = 0
        self.reset()

    def status(self):
        self.write(0xf32d)
        self.i2c.readfrom_into(self._addr, self._rb)
        return self._rb[0]*256 + self._rb[1]

    def clear_status(self):
        self.write(0x3041)

    def write(self, cmd):
        self._tb[0] = cmd>>8
        self._tb[1] = cmd
        self.i2c.writeto(self._addr, self._tb)

    def reset(self):
        self.write(0x30a2)
    
    def heater(self, on=0):
        if on: self.write(0x306d)
        else:  self.write(0x3066)
    
    def config(self, mode = 0x240b, delay = 6, decimal = 1):
        t = mode >> 8
        self._mode = 1 if t == 0x24 or t == 0x2C else 0
        self._cmd = mode
        self._delay = delay
        self._decimal = decimal
        self.write(mode)
        
    def measure(self):
        if self._mode:
            self.write(self._cmd)
            sleep_ms(self._delay)
        self.write(0xe000)
        self.i2c.readfrom_into(self._addr, self._ht)
        self._T = self._ht[0]*256+self._ht[1]
        self._H = self._ht[3]*256+self._ht[4]

    def humidity(self):
        return round(100*self._H/65535, self._decimal)

    def temperature(self):
        return round(175*self._T/65535 - 45, self._decimal)

    def ht(self):
        return self.humidity(), self.temperature()
