"""
    mpy drive for BMP180 Digital Pressure Sensor

    Author: shaoziyang
    Date:   2018.2

    http://www.micropython.org.cn

"""
import time
from machine import I2C

BMP180_I2C_ADDR = const(0x77)

class BMP180():
    def __init__(self, i2c):
        self.i2c = i2c
        self.AC1 = self.short(self.get2Reg(0xAA))
        self.AC2 = self.short(self.get2Reg(0xAC))
        self.AC3 = self.short(self.get2Reg(0xAE))
        self.AC4 = self.get2Reg(0xB0)
        self.AC5 = self.get2Reg(0xB2)
        self.AC6 = self.get2Reg(0xB4)
        self.B1 = self.short(self.get2Reg(0xB6))
        self.B2 = self.short(self.get2Reg(0xB8))
        self.MB = self.short(self.get2Reg(0xBA))
        self.MC = self.short(self.get2Reg(0xBC))
        self.MD = self.short(self.get2Reg(0xBE))
        self.UT = 0
        self.UP = 0
        self.T = 0
        self.P = 0
        self.version = '2.0'

    def short(self, dat):
        if dat > 32767:
            return dat - 65536
        else:
            return dat

    # set reg
    def	setReg(self, reg, dat):
        self.i2c.writeto(BMP180_I2C_ADDR, bytearray([reg, dat]))
		
    # get reg
    def	getReg(self, reg):
        self.i2c.writeto(BMP180_I2C_ADDR, bytearray([reg]))
        t =	self.i2c.readfrom(BMP180_I2C_ADDR, 1)
        return t[0]
	
    # get two reg
    def	get2Reg(self, reg):
        self.i2c.writeto(BMP180_I2C_ADDR, bytearray([reg]))
        t =	self.i2c.readfrom(BMP180_I2C_ADDR, 2)
        return t[0]*256 + t[1]

    # start measure
    def measure(self):
        self.setReg(0xF4, 0x2E)
        time.sleep_ms(5)
        self.UT = self.get2Reg(0xF6)
        self.setReg(0xF4, 0x34)
        time.sleep_ms(5)
        self.UP = self.get2Reg(0xF6)

    # get Temperature and Pressure
    def get(self):
        self.measure()
        X1 = (self.UT - self.AC6) * self.AC5/(1<<15)
        X2 = self.MC * (1<<11) / (X1 + self.MD)
        B5 = X1 + X2
        self.T = (B5 + 8)/160
        B6 = B5 - 4000
        X1 = (self.B2 * (B6*B6/(1<<12))) / (1<<11)
        X2 = (self.AC2 * B6)/(1<<11)
        X3 = X1 + X2
        B3 = ((self.AC1*4+X3) + 2)/4
        X1 = self.AC3 * B6 / (1<<13)
        X2 = (self.B1 * (B6*B6/(1<<12))) / (1<<16)
        X3 = (X1 + X2 + 2)/4
        B4 = self.AC4 * (X3 + 32768)/(1<<15)
        B7 = (self.UP-B3) * 50000
        if B7 < 0x80000000:
            p = (B7*2)/B4
        else:
            p = (B7/B4) * 2
        X1 = (p/(1<<8))*(p/(1<<8))
        X1 = (X1 * 3038)/(1<<16)
        X2 = (-7357*p)/(1<<16)
        self.P = p + (X1 + X2 + 3791)/16
        return [self.T, self.P]

    # get Temperature in Celsius
    def getTemp(self):
        self.get()
        return self.T
        
    # get Pressure in Pa
    def getPress(self):
        self.get()
        return self.P
    
    # Calculating absolute altitude
    def getAltitude(self):
        return 44330*(1-(self.getPress()/101325)**(1/5.255))

