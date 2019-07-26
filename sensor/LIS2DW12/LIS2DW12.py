# LIS2DW12 3-axis motion seneor micropython drive
# ver: 1.0
# License: MIT
# Author: shaoziyang (shaoziyang@micropython.org.cn)
# v1.0 2019.7

LIS2DW12_CTRL1 = const(0x20)
LIS2DW12_CTRL2 = const(0x21)
LIS2DW12_CTRL3 = const(0x22)
LIS2DW12_CTRL6 = const(0x25)
LIS2DW12_STATUS = const(0x27)
LIS2DW12_OUT_T_L = const(0x0D)
LIS2DW12_OUT_X_L = const(0x28)
LIS2DW12_OUT_Y_L = const(0x2A)
LIS2DW12_OUT_Z_L = const(0x2C)

LIS2DW12_SCALE = ('2g', '4g', '8g', '16g')

class LIS2DW12():
    def __init__(self, i2c, addr = 0x19):
        self.i2c = i2c
        self.addr = addr
        self.tb = bytearray(1)
        self.rb = bytearray(1)
        self.oneshot = False
        self.irq_v = [0, 0, 0]
        self._power = 0x20
        # ODR=5 MODE=0 LP=1
        self.setreg(LIS2DW12_CTRL1, 0x51)
        # BDU=1
        self.setreg(LIS2DW12_CTRL2, 0x0C)
        # SLP_MODE_SEL=1
        self.setreg(LIS2DW12_CTRL3, 0x02)
        # scale=2G
        self._scale = 0
        self.scale(self._scale)
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

    def r_w_reg(self, reg, dat, mask):
        self.getreg(reg)
        self.rb[0] = (self.rb[0] & mask) | dat
        self.setreg(reg, self.rb[0])

    def oneshot_mode(self, oneshot=None):
        if oneshot is None:
            return self.oneshot
        else:
            self.oneshot = oneshot
            d = 8 if oneshot else 0
            self.r_w_reg(LIS2DW12_CTRL1, d, 0xF3)

    def ONE_SHOT(self):
        if self.oneshot:
            self.r_w_reg(LIS2DW12_CTRL3, 1, 0xFE)
            while 1:
                if (self.getreg(LIS2DW12_CTRL3) & 0x01) == 0:
                    return

    def x_raw(self):
        self.ONE_SHOT()
        return self.int16(self.get2reg(LIS2DW12_OUT_X_L))>>2

    def y_raw(self):
        self.ONE_SHOT()
        return self.int16(self.get2reg(LIS2DW12_OUT_Y_L))>>2

    def z_raw(self):
        self.ONE_SHOT()
        return self.int16(self.get2reg(LIS2DW12_OUT_Z_L))>>2

    def get_raw(self):
        self.ONE_SHOT()
        self.irq_v[0] = self.int16(self.get2reg(LIS2DW12_OUT_X_L))>>2
        self.irq_v[1] = self.int16(self.get2reg(LIS2DW12_OUT_Y_L))>>2
        self.irq_v[2] = self.int16(self.get2reg(LIS2DW12_OUT_Z_L))>>2
        return self.irq_v

    def mg(self, reg):
        return round(self.int16(self.get2reg(reg)) * 0.061 * (1 << self._scale))

    def x(self):
        self.ONE_SHOT()
        return self.mg(LIS2DW12_OUT_X_L)

    def y(self):
        self.ONE_SHOT()
        return self.mg(LIS2DW12_OUT_Y_L)

    def z(self):
        self.ONE_SHOT()
        return self.mg(LIS2DW12_OUT_Z_L)

    def get(self):
        self.ONE_SHOT()
        self.irq_v[0] = self.mg(LIS2DW12_OUT_X_L)
        self.irq_v[1] = self.mg(LIS2DW12_OUT_Y_L)
        self.irq_v[2] = self.mg(LIS2DW12_OUT_Z_L)
        return self.irq_v

    def temperature(self):
        try:
            return self.int16(self.get2reg(LIS2DW12_OUT_T_L))/256 + 25
        except MemoryError:
            return self.temperature_irq()

    def temperature_irq(self):
        self.getreg(LIS2DW12_OUT_T_L+1)
        if self.rb[0] & 0x80: self.rb[0] -= 256
        return self.rb[0] + 25

    def scale(self, dat=None):
        if dat is None:
            return LIS2DW12_SCALE[self._scale]
        else:
            if type(dat) is str:
                if not dat in LIS2DW12_SCALE: return
                self._scale = LIS2DW12_SCALE.index(dat)
            else: return
            self.r_w_reg(LIS2DW12_CTRL6, self._scale<<4, 0xCF)

    def power(self, on=None):
        if on is None:
            return self._power > 0
        else:
            if on:
                self.r_w_reg(LIS2DW12_CTRL1, self._power, 0x0F)
                self._power = 0
            else:
                self._power = self.getreg(LIS2DW12_CTRL1) & 0xF0
                self.r_w_reg(LIS2DW12_CTRL1, 0, 0x0F)
