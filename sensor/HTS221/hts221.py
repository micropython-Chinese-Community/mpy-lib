# HTS221 Humidity and temperature micropython drive
# ver: 2.0
# License: MIT
# Author: shaoziyang (shaoziyang@micropython.org.cn)
# v1.0 2016.4
# v2.0 2019.7

from machine import I2C

class HTS221(object):
    def __init__(self, i2c):
        self.i2c = i2c
        self.addr = 0x5F
        # data buffer
        self.tb = bytearray(1)
        self.rb = bytearray(1)
        self.oneshot = False
        self.irq_v = [0, 0]
        # HTS221 Temp Calibration registers
        self.T0_OUT = self.int16(self.get2reg(0x3C))
        self.T1_OUT = self.int16(self.get2reg(0x3E))
        t = self.getreg(0x35) % 16
        self.T0_degC = self.getreg(0x32) + (t%4) * 256
        self.T1_degC = self.getreg(0x33) + (t//4) * 256
        # HTS221 Humi Calibration registers
        self.H0_OUT = self.int16(self.get2reg(0x36))
        self.H1_OUT = self.int16(self.get2reg(0x3A))
        self.H0_rH = self.getreg(0x30) * 5
        self.H1_rH = self.getreg(0x31) * 5
        self.K1 = (self.T1_degC - self.T0_degC) / (self.T1_OUT - self.T0_OUT)
        self.K2 = (self.H1_rH - self.H0_rH) / (self.H1_OUT - self.H0_OUT)
        # set av conf: T=4 H=8
        self.setreg(0x10, 0x26)
        # set CTRL_REG1: PD=1 BDU=1 ODR=1
        self.setreg(0x20, 0x85)
        self.oneshot_mode(0)

    def oneshot_mode(self, oneshot = None):
        if oneshot is None:
            return self.oneshot
        else:
            self.getreg(0x20)
            self.oneshot = oneshot
            if oneshot: self.rb[0] &= 0xFC
            else: self.rb[0] |= 0x01
            self.setreg(0x20, self.rb[0])

    def ONE_SHOT(self, b):
        if self.oneshot:
            self.setreg(0x21, self.getreg(0x21) | 0x01)
            self.getreg(0x2d - b*2)
            while 1:
                if self.getreg(0x27) & b:
                    return

    def int16(self, d):
        return d if d < 0x8000 else d - 0x10000

    def setreg(self, reg, dat):
        self.tb[0] = dat
        self.i2c.writeto_mem(self.addr, reg, self.tb)

    def getreg(self, reg):
        self.i2c.readfrom_mem_into(self.addr, reg, self.rb)
        return self.rb[0]
   
    def get2reg(self, reg):
        return self.getreg(reg) + self.getreg(reg+1) * 256

    # calculate Temperature
    def temperature(self):
        try:
            self.ONE_SHOT(1)
            return round((self.T0_degC + (self.int16(self.get2reg(0x2A)) - self.T0_OUT) * self.K1)/8, 1)
        except MemoryError:
            return self.temperature_irq()

    # calculate Humidity
    def humidity(self):
        try:
            self.ONE_SHOT(2)
            return round((self.H0_rH + (self.int16(self.get2reg(0x28)) - self.H0_OUT) * self.K2)/10, 1)
        except MemoryError:
            return self.humidity_irq()

    def get(self):
        try:
            return self.temperature(), self.humidity()
        except MemoryError:
            return self.get_irq()

    def temperature_irq(self):
        self.ONE_SHOT(1)
        return (self.T0_degC + (self.int16(self.get2reg(0x2A)) - self.T0_OUT) * (self.T1_degC - self.T0_degC) // (self.T1_OUT - self.T0_OUT)) >> 3

    def humidity_irq(self):
        self.ONE_SHOT(2)
        return (self.H0_rH + (self.int16(self.get2reg(0x28)) - self.H0_OUT) * (self.H1_rH - self.H0_rH) // (self.H1_OUT - self.H0_OUT))//10

    def get_irq(self):
        self.irq_v[0] = self.temperature_irq()
        self.irq_v[1] = self.humidity_irq()
        return tuple(self.irq_v)

    def power(self, on=None):
        self.getreg(0x20)
        if on is None: return self.rb[0] & 0x80 > 0
        elif on: self.rb[0] |= 0x80
        else: self.rb[0] &= 0x7F 
        self.setreg(0x20, self.rb[0])
