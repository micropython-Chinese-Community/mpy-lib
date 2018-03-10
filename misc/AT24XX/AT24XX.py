'''
    AT24C32 EEPROM drive

    Author: shaoziyang
    Date:   2018.3

    http://www.micropython.org.cn
'''
from machine import I2C

AT24CXX_I2C_ADDRESS = (80)

class AT24XX():
    def __init__(self, i2c):
        self.i2c = i2c

    def write_byte(self, addr, dat):
        self.i2c.writeto(AT24CXX_I2C_ADDRESS, bytearray([addr//256, addr, dat]))

    def read_byte(self, addr):
        self.i2c.writeto(AT24CXX_I2C_ADDRESS, bytearray([addr//256, addr]))
        t = self.i2c.readfrom(AT24CXX_I2C_ADDRESS, 1)
        return t[0]

    def write_word(self, addr, dat):
        self.i2c.writeto(AT24CXX_I2C_ADDRESS, bytearray([addr//256, addr, dat//256, dat]))

    def read_word(self, addr):
        self.i2c.writeto(AT24CXX_I2C_ADDRESS, bytearray([addr//256, addr]))
        t = self.i2c.readfrom(AT24CXX_I2C_ADDRESS, 2)
        return t[0]*256 + t[1]

    def write_dword(self, addr, dat):
        self.i2c.writeto(AT24CXX_I2C_ADDRESS, bytearray([addr//256, addr, dat>>24, dat>>16, dat>>8, dat]))

    def read_dword(self, addr):
        self.i2c.writeto(AT24CXX_I2C_ADDRESS, bytearray([addr//256, addr]))
        t = self.i2c.readfrom(AT24CXX_I2C_ADDRESS, 4)
        return (t[0]<<24) + (t[1]<<16) + (t[2]<<8) + t[3]

    def write_buf(self, addr, buf):
        self.i2c.writeto(AT24CXX_I2C_ADDRESS, bytearray([addr//256, addr]) + buf)
        
    def read_buf(self, addr, num):
        self.i2c.writeto(AT24CXX_I2C_ADDRESS, bytearray([addr//256, addr]))
        return self.i2c.readfrom(AT24CXX_I2C_ADDRESS, num)

