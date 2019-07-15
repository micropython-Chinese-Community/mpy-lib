# LPS22HB/HH pressure seneor micropython drive
# ver: 2.0
# License: MIT
# Author: shaoziyang (shaoziyang@micropython.org.cn)
# v1.0 2016.4
# v2.0 2019.7

LPS22_CTRL_REG1    = const(0x10)
LPS22_TEMP_OUT_L   = const(0x2B)
LPS22_PRESS_OUT_XL = const(0x28)
LPS22_PRESS_OUT_L  = const(0x29)

class LPS22():
    def __init__(self, i2c, addr = 0x5D):
        self.i2c = i2c
        self.addr = addr
        self.tb = bytearray(1)
        self.rb = bytearray(1)
        self.irq_v = [0, 0]
        # ODR=1 EN_LPFP=1
        self.setreg(LPS22_CTRL_REG1, 0x18)

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

    def power(self):
        t = self.getreg(LPS22HB_CTRL_REG1, LPS22HB_ADDRESS) & 0x0F
        self.setreg(t|0x10, LPS22HB_CTRL_REG1, LPS22HB_ADDRESS)
        self.LPS22HB_ON = True

    def LPS22HB_poweroff(self):
        t = self.getreg(LPS22HB_CTRL_REG1, LPS22HB_ADDRESS) & 0x0F
        self.setreg(t, LPS22HB_CTRL_REG1, LPS22HB_ADDRESS)
        self.LPS22HB_ON = False

    def temperature(self):
        try:
            return self.int16(self.get2reg(LPS22_TEMP_OUT_L))/100
        except MemoryError:
            return self.temperature_irq()

    def pressure(self):
        try:
            return (self.getreg(LPS22_PRESS_OUT_XL) + self.get2reg(LPS22_PRESS_OUT_L) * 256)/4096
        except MemoryError:
            return self.pressure_irq()

    def get(self):
        try:
            return self.temperature(), self.pressure()
        except MemoryError:
            return self.get_irq()

    def altitude(self):
        return (((1013.25 / self.pressure())**(1/5.257)) - 1.0) * (self.temperature() + 273.15) / 0.0065

    def temperature_irq(self):
        return self.int16(self.get2reg(LPS22_TEMP_OUT_L))//100

    def pressure_irq(self):
        return self.get2reg(LPS22_PRESS_OUT_L) >> 4

    def get_irq(self):
        self.irq_v[0] = self.temperature_irq()
        self.irq_v[1] = self.pressure_irq()
        return self.irq_v
