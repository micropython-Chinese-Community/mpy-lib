'''
    mpy drive for INA219 Bidirectional Current/Power Monitor

    Author: shaoziyang
    Date:   2024.5

    http://www.micropython.org.cn

'''
from micropython import const

INA219_ADDR = const(64)

class INA219():
    def __init__(self, i2c):
        self.i2c = i2c
        self.rb = bytearray(2)
        self.tb = bytearray(2)
        self.setreg(0, 0x8000)  # reset
        self.setreg(0, 0x3fff)
        self.calreg(4096)       # default Calibration Register

    def setreg(self, reg, dat):
        self.tb[0] = dat//256
        self.tb[1] = dat
        self.i2c.writeto_mem(INA219_ADDR, reg, self.tb)

    def getreg(self, reg):
        self.i2c.readfrom_mem_into(INA219_ADDR, reg, self.rb)
        return self.rb[0]*256+self.rb[1]

    def calreg(self, value=None):
        if value == None:
            return self.getreg(5)
        else:
            self.setreg(5, value)

    def volt(self):
        return self.getreg(2)/2000
    
    def current(self):
        return self.getreg(4)/10000

    def power(self):
        return self.getreg(3)/500

