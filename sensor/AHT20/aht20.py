'''
    mpy drive for AHT20 Sensor

    Author: shaoziyang
    Date:   2023.8

    http://www.micropython.org.cn

'''
from machine import I2C
from micropython import const
from time import sleep_ms

CMD_INIT = const(0xBE)
CMD_MEASURE = const(0xAC)
CMD_RESET = const(0xBA)

class AHT20:

    def __init__(self, i2c):
        self.i2c = i2c
        self.addr = 56
        self.tb = bytearray(3)
        self.rb = bytearray(6)
        self._H = 0
        self._T = 0
        self.init()

    def set(self, cmd, dat):
        self.tb[0] = cmd
        self.tb[1] = dat >> 8
        self.tb[2] = dat
        self.i2c.writeto_mem(self.addr, cmd, self.tb)

    def get(self):
        self.i2c.readfrom_into(self.addr, self.rb)

    def init(self):
        self.set(CMD_INIT, 0x0800)

    def reset(self):
        self.set(CMD_RESET, 0)

    def measure(self):
        self.set(CMD_MEASURE, 0x3300)
        sleep_ms(75)
        self.get()
        self._H = (self.rb[1]<<12)+(self.rb[2]<<4)+(self.rb[3]>>4)
        self._T = ((self.rb[3]%16)<<16)+(self.rb[4]<<8)+self.rb[5]

    def Humi(self):
        return (self._H*100)/(1<<20)

    def Temp(self):
        return (self._T*200)/(1<<20)-50


