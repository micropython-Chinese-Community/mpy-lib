# LIS2MDL magnetic seneor micropython drive
# ver: 1.0
# License: MIT
# Author: shaoziyang (shaoziyang@micropython.org.cn)
# v1.0 2019.7

LIS2MDL_CFG_REG_A = const(0x60)
LIS2MDL_CFG_REG_C = const(0x62)
LIS2MDL_STATUS_REG = const(0x67)
LIS2MDL_OUTX_L_REG = const(0x68)
LIS2MDL_OUTY_L_REG = const(0x6A)
LIS2MDL_OUTZ_L_REG = const(0x6C)

class LIS2MDL():
    def __init__(self, i2c):
        self.i2c = i2c
        self.addr = 0x1E
        self.tb = bytearray(1)
        self.rb = bytearray(1)
        # TEMP_EN=1 LP=0 ODR=0 MD=0
        self.setreg(LIS2MDL_CFG_REG_A, 0x80)
        # BDU=1
        self.setreg(LIS2MDL_CFG_REG_C, 0x10)
        self.oneshot = False
        self.irq_v = [0, 0, 0]

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

    def oneshot_mode(self, oneshot=None):
        if oneshot is None:
            return self.oneshot
        else:
            self.get2reg(LIS2MDL_OUTX_L_REG)
            self.get2reg(LIS2MDL_OUTY_L_REG)
            self.get2reg(LIS2MDL_OUTZ_L_REG)
            self.getreg(LIS2MDL_CFG_REG_A)
            self.oneshot = oneshot
            self.rb[0] &= 0xFC
            if oneshot:
                self.rb[0] |= 0x01
            self.setreg(LIS2MDL_CFG_REG_A, self.rb[0])

    def ONE_SHOT(self):
        if self.oneshot:
            self.oneshot_mode(1)
            while 1:
                if self.getreg(LIS2MDL_STATUS_REG) & 0x08:
                    return

    def x_raw(self):
        self.ONE_SHOT()
        return self.int16(self.get2reg(LIS2MDL_OUTX_L_REG))

    def y_raw(self):
        self.ONE_SHOT()
        return self.int16(self.get2reg(LIS2MDL_OUTY_L_REG))

    def z_raw(self):
        self.ONE_SHOT()
        return self.int16(self.get2reg(LIS2MDL_OUTZ_L_REG))

    def get_raw(self):
        self.ONE_SHOT()
        self.irq_v[0] = self.int16(self.get2reg(LIS2MDL_OUTX_L_REG))
        self.irq_v[1] = self.int16(self.get2reg(LIS2MDL_OUTY_L_REG))
        self.irq_v[2] = self.int16(self.get2reg(LIS2MDL_OUTZ_L_REG))
        return self.irq_v

    // unit uT
    def x(self):
        return self.x_raw()*3//20

    // unit uT
    def y(self):
        return self.y_raw()*3//20

    // unit uT
    def z(self):
        return self.z_raw()*3//20

    // uint uT
    def get(self):
        self.ONE_SHOT()
        self.irq_v[0] = self.int16(self.get2reg(LIS2MDL_OUTX_L_REG))*3//20
        self.irq_v[1] = self.int16(self.get2reg(LIS2MDL_OUTY_L_REG))*3//20
        self.irq_v[2] = self.int16(self.get2reg(LIS2MDL_OUTZ_L_REG))*3//20
        return self.irq_v
