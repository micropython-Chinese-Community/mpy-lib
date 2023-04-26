from machine import I2C

class SC7A20:
    
    def __init__(self, i2c, SDO = 1):
        self.i2c = i2c
        self.ADDR = 0x19 if SDO == 1 else 0x18
        self._ODR = 4
        self._LPen = 1
        self._FS = 0
        self._HR = 1
        self.tb = bytearray(1)
        self.rb = bytearray(1)
        self.init()
        
    def reg_set(self, reg, val):
        self.tb[0] = val
        self.i2c.writeto_mem(self.ADDR, reg, self.tb)
        
    def reg_get(self, reg):
        self.i2c.readfrom_mem_into(self.ADDR, reg, self.rb)
        return self.rb[0]
        
    def rw_reg(self, reg, dat, mask):
        self.reg_get(reg)
        self.rb[0] = (self.rb[0] & mask) | dat
        self.reg_set(reg, self.rb[0])
        
    def ODR(self, odr = None):
        if odr != None:
            self._ODR = odr
            self.rw_reg(0x20, odr<<4, 0x0F)
        else:
            return self._ODR
    
    def LP(self, lp = None):
        if lp != None:
            self._LPen = lp
            self.rw_reg(0x20, lp<<3, 0x08)        
        else:
            return self._LPen
    
    def FS(self, fs = None):
        if fs != None:
            self._FS = fs
            self.rw_reg(0x23, fs<<4, 0xCF) 
        else:
            return self._FS
 
    def HR(self, hr = None):
        if hr != None:
            self._HR = hr
            self.rw_reg(0x23, hr<<3, 0x08) 
        else:
            return self._HR
        
    def on(self):
        self.ODR(self._ODR)
        
    def off(self):
        self.ODR(0)
    
    def init(self):
        # enable TEMP
        self.reg_set(0x1F, 255)
        # ODR 4 (50Hz), LPEN = 1, XYZen = 1
        self.LP(1)
        # BDU = BLE = 0, FS = 0 (2G), HR = 1
        self.FS(0)
        self.HR(1)
        self.on()
        # int lock
        self.reg_set(0x24, 0x0F)

    def int16(self, d):
        return d if d < 0x8000 else d - 0x10000

    def T(self):
        return self.reg_get(0x0D)
        
    def rawx(self):
        return self.reg_get(0x28) + self.reg_get(0x29)*256
        
    def rawy(self):
        return self.reg_get(0x2A) + self.reg_get(0x2B)*256
        
    def rawz(self):
        return self.reg_get(0x2C) + self.reg_get(0x2D)*256

    def x(self):
        return self.int16(self.rawx())>>(4-self._FS)

    def y(self):
        return self.int16(self.rawy())>>(4-self._FS)

    def z(self):
        return self.int16(self.rawz())>>(4-self._FS)

    

