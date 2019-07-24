# STTS751 temperature seneor micropython drive
# ver: 1.0
# License: MIT
# Author: shaoziyang (shaoziyang@micropython.org.cn)
# v1.0 2019.7

STTS751_RESOLUTION = (8, 0, 4, 12, 10, 11, 9, 12)
STTS751_REG_STATUS = const(1)
STTS751_REG_CONFIG = const(3)
STTS751_REG_CONRAT = const(4)
STTS751_REG_TEMPVH = const(0)
STTS751_REG_TEMPVL = const(2)
STTS751_REG_TEMPHH = const(5)
STTS751_REG_TEMPHL = const(6)
STTS751_REG_TEMPLH = const(7)
STTS751_REG_TEMPLL = const(8)
STTS751_REG_ONESHOT = const(15)
STTS751_REG_THERM = const(32)
STTS751_REG_THERMHYS = const(33)

class STTS751():
    def __init__(self, i2c):
        self.i2c = i2c
        self.addr = 0x4A
        self.tb = bytearray(1)
        self.rb = bytearray(1)
        self.oneshot = False
        self.oneshot_mode(False)

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

    def resolution(self, res = None):
        self.getreg(STTS751_REG_CONFIG)
        if res is None:
            return STTS751_RESOLUTION[(self.rb[0] & 0x0C)//4 + 4]
        else:
            if res > 12 or res < 9: return
            self.rb[0] = (self.rb[0] & 0xF3) | STTS751_RESOLUTION[res-9]
            self.setreg(STTS751_REG_CONFIG, self.rb[0])

    def oneshot_mode(self, oneshot=None):
        if oneshot is None:
            return self.oneshot
        else:
            self.getreg(STTS751_REG_CONFIG)
            self.oneshot = oneshot
            if oneshot: self.rb[0] |= 0x40
            else: self.rb[0] &= 0xBF
            self.setreg(STTS751_REG_CONFIG, self.rb[0])

    def ONE_SHOT(self):
        if self.oneshot:
            self.setreg(STTS751_REG_ONESHOT, 1)
            while 1:
                if self.getreg(STTS751_REG_STATUS) < 0x80:
                    return

    def temperature(self):
        try:
            self.ONE_SHOT()
            return self.int16((self.getreg(STTS751_REG_TEMPVH)<<8) + self.getreg(STTS751_REG_TEMPVL))/256
        except MemoryError:
            return self.temperature_irq()
 
    def temperature_irq(self):
        self.ONE_SHOT()
        self.getreg(STTS751_REG_TEMPVH)
        return self.rb[0] if self.rb[0] < 128 else self.rb[0] - 256


