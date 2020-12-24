'''
    mpy drive for SHT20 Humidity and Temperature Sensor

    Author: shaoziyang
    Date:   2020.12

    http://www.micropython.org.cn

'''
from micropython import const
from time import sleep_ms

SHT20_I2C_ADDR = const(0x40)

class SHT20():

    def __init__(self, i2c):
        self.i2c = i2c
        self.tb = bytearray(1)
        self.rb = bytearray(1)
        self.ht = bytearray(3)
        self.reset()

    def setreg(self, reg, dat):
        self.tb[0] = dat
        self.i2c.writeto_mem(SHT20_I2C_ADDR, reg, self.tb)

    def getreg(self, reg):
        self.i2c.readfrom_mem_into(SHT20_I2C_ADDR, reg, self.rb)
        return self.rb[0]

    def write(self, cmd):
        self.tb[0] = cmd
        self.i2c.writeto(SHT20_I2C_ADDR, self.tb)

    def reset(self):
        self.write(0xfe)
    
    def measure(self, cmd, delay):
        self.write(cmd)
        sleep_ms(delay)
        self.i2c.readfrom_into(SHT20_I2C_ADDR, self.ht)

    def humi_raw(self):
        self.measure(0xf5, 30)
        return self.ht[0]*256+self.ht[1]

    def temperature_raw(self):
        self.measure(0xf3, 85)
        return self.ht[0]*256+self.ht[1]

    def humi(self, raw):
        return (125*raw//65536) -6

    def temperature(self, raw):
        return 175.72*raw/65536 - 46.85
