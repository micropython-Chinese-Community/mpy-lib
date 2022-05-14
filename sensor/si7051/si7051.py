from machine import I2C
from time import sleep_ms

SI7051_I2C_ADDR = 0x40
SI7051_CMD_HOLD_MODE = b'\xE3'
SI7051_CMD_NO_HOLD_MODE = b'\xF3'
SI7051_CMD_RESET = b'\xFE'
SI7051_CMD_WRITE_USER_REG1 = b'\xE6'
SI7051_CMD_READ_USER_REG1 = b'\xE7'
SI7051_CMD_READ_ID1 = b'\xFA\x0F'
SI7051_CMD_READ_ID2 = b'\xFC\xC9'
SI7051_CMD_READ_REV = b'\x84\xB8'

class si7051():
    def __init__(self, i2c):
        self.i2c = i2c

    # get reg
    def getReg(self, buf, n=1):
        self.i2c.writeto(SI7051_I2C_ADDR, buf)
        t = self.i2c.readfrom(SI7051_I2C_ADDR, n)
        return t

    def ID(self):
        a = self.getReg(SI7051_CMD_READ_ID1, 4)
        b = self.getReg(SI7051_CMD_READ_ID2, 4)
        return hex(int.from_bytes(a+b,''))[2:]

    def REV(self):
        a = self.getReg(SI7051_CMD_READ_REV)
        return a[0]

    def UserReg(self, reg=''):
        if reg == '':
            return self.getReg(SI7051_CMD_READ_USER_REG1)[0]
        else:
            self.i2c.writeto(SI7051_I2C_ADDR, bytearray(SI7051_CMD_WRITE_USER_REG1) + bytearray([reg]))

    def name(self):
        a = self.getReg(SI7051_CMD_READ_ID2, 4)[0]
        return 'si70'+str(a)

    def Temperature(self, digital=2, delay=10):
        self.i2c.writeto(SI7051_I2C_ADDR, SI7051_CMD_NO_HOLD_MODE)
        sleep_ms(delay)
        a = self.i2c.readfrom(SI7051_I2C_ADDR, 2)
        b = a[0]*256 + a[1]
        return round(b*175.72/65536 - 46.85, digital)

