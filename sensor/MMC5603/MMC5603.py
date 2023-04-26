from machine import I2C
from micropython import const

MMC5603ADDR = const(48)

class MMC5603:
    
    def __init__(self, i2c):
        self.i2c = i2c
        self.tb = bytearray(1)
        self.rb = bytearray(1)
        self._rawx = 0
        self._rawy = 0
        self._rawz = 0
        if self.reg_get(0x39) != 0x10:
           raise Exception('MMC5603 ID error!')
        self.on()
    
    def on(self):
        # ODR = 10
        self.reg_set(0x1A, 10)
        self.reg_set(0x1C, 0x03)
        # set CONTINUOUS mode
        self.reg_set(0x1B, 0xA0)
        self.reg_set(0x1D, 0x1B)

    def off(self):
        # soft reset
        self.reg_set(0x1C, 0x80)        

    def reg_set(self, reg, val):
        self.tb[0] = val
        self.i2c.writeto_mem(MMC5603ADDR, reg, self.tb)
        
    def reg_get(self, reg):
        self.i2c.readfrom_mem_into(MMC5603ADDR, reg, self.rb)
        return self.rb[0]        
    
    def rawx(self):
        self._rawx = self.reg_get(0)*256+self.reg_get(1)-32768
        return self._rawx

    def rawy(self):
        self._rawy = self.reg_get(2)*256+self.reg_get(3)-32768
        return self._rawy

    def rawz(self):
        self._rawz = self.reg_get(4)*256+self.reg_get(5)-32768
        return self._rawz
    
    def x(self):
        return self.rawx() // 10

    def y(self):
        return self.rawy() // 10

    def z(self):
        return self.rawz() // 10
    
    def T(self):
        self.reg_set(0x1B, 0xA3)
        return self.reg_get(9)*0.8-75

