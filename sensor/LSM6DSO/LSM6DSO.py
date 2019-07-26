# LSM6DSO 3D accelerometer and 3D gyroscope seneor micropython drive
# ver: 1.0
# License: MIT
# Author: shaoziyang (shaoziyang@micropython.org.cn)
# v1.0 2019.7

LSM6DSO_CTRL1_XL = const(0x10)
LSM6DSO_CTRL2_G = const(0x11)
LSM6DSO_CTRL3_C = const(0x12)
LSM6DSO_CTRL6_C = const(0x15)
LSM6DSO_CTRL8_XL = const(0x17)
LSM6DSO_STATUS = const(0x1E)
LSM6DSO_OUT_TEMP_L = const(0x20)
LSM6DSO_OUTX_L_G = const(0x22)
LSM6DSO_OUTY_L_G = const(0x24)
LSM6DSO_OUTZ_L_G = const(0x26)
LSM6DSO_OUTX_L_A = const(0x28)
LSM6DSO_OUTY_L_A = const(0x2A)
LSM6DSO_OUTZ_L_A = const(0x2C)

LSM6DSO_SCALEA = ('2g', '16g', '4g', '8g')
LSM6DSO_SCALEG = ('250', '125', '500', '', '1000', '', '2000')

class LSM6DSO():
    def __init__(self, i2c, addr = 0x6B):
        self.i2c = i2c
        self.addr = addr
        self.tb = bytearray(1)
        self.rb = bytearray(1)
        self.oneshot = False
        self.irq_v = [[0, 0, 0], [0, 0, 0]]
        self._power = True
        self._power_a = 0x10
        self._power_g = 0x10
        # ODR_XL=1 FS_XL=0
        self.setreg(LSM6DSO_CTRL1_XL, 0x10)
        # ODR_G=1 FS_125=1
        self.setreg(LSM6DSO_CTRL2_G, 0x12)        
        # BDU=1 IF_INC=1
        self.setreg(LSM6DSO_CTRL3_C, 0x44)
        self.setreg(LSM6DSO_CTRL8_XL, 0)
        # scale=2G
        self._scale_a = 0
        self._scale_g = 0
        self._scale_a_c = 1
        self._scale_g_c = 1
        self.scale_a('2g')
        self.scale_g('125')

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

    def ax_raw(self):
        return self.int16(self.get2reg(LSM6DSO_OUTX_L_A))

    def ay_raw(self):
        return self.int16(self.get2reg(LSM6DSO_OUTY_L_A))

    def az_raw(self):
        return self.int16(self.get2reg(LSM6DSO_OUTZ_L_A))

    def gx_raw(self):
        return self.int16(self.get2reg(LSM6DSO_OUTX_L_G))

    def gy_raw(self):
        return self.int16(self.get2reg(LSM6DSO_OUTY_L_G))

    def gz_raw(self):
        return self.int16(self.get2reg(LSM6DSO_OUTZ_L_G))

    def mg(self, reg):
        return round(self.int16(self.get2reg(reg)) * 0.061 * self._scale_a_c)

    def mdps(self, reg):
        return round(self.int16(self.get2reg(reg)) * 4.375 * self._scale_g_c) 

    def ax(self):
        return self.mg(LSM6DSO_OUTX_L_A)

    def ay(self):
        return self.mg(LSM6DSO_OUTY_L_A)

    def az(self):
        return self.mg(LSM6DSO_OUTZ_L_A)

    def gx(self):
        return self.mdps(LSM6DSO_OUTX_L_G)

    def gy(self):
        return self.mdps(LSM6DSO_OUTY_L_G)

    def gz(self):
        return self.mdps(LSM6DSO_OUTZ_L_G)

    def get_a(self):
        self.irq_v[0][0] = self.ax()
        self.irq_v[0][1] = self.ay()
        self.irq_v[0][2] = self.az()        
        return self.irq_v[0]

    def get_g(self):
        self.irq_v[1][0] = self.gx()
        self.irq_v[1][1] = self.gy()
        self.irq_v[1][2] = self.gz()        
        return self.irq_v[1]

    def get(self):
        self.get_a()
        self.get_g()
        return self.irq_v

    def get_a_raw(self):
        self.irq_v[0][0] = self.ax_raw()
        self.irq_v[0][1] = self.ay_raw()
        self.irq_v[0][2] = self.az_raw()        
        return self.irq_v[0]

    def get_g(self):
        self.irq_v[1][0] = self.gx_raw()
        self.irq_v[1][1] = self.gy_raw()
        self.irq_v[1][2] = self.gz_raw()        
        return self.irq_v[1]

    def get(self):
        self.get_a_raw()
        self.get_g_raw()
        return self.irq_v

    def temperature(self):
        try:
            return self.int16(self.get2reg(LSM6DSO_OUT_TEMP_L))/256 + 25
        except MemoryError:
            return self.temperature_irq()

    def temperature_irq(self):
        self.getreg(LSM6DSO_OUT_TEMP_L+1)
        if self.rb[0] & 0x80: self.rb[0] -= 256
        return self.rb[0] + 25

    def scale_a(self, dat=None):
        if dat is None:
            return LSM6DSO_SCALEA[self._scale_a]
        else:
            if type(dat) is str:
                if not dat in LSM6DSO_SCALEA: return
                self._scale_a = LSM6DSO_SCALEA.index(dat)
                self._scale_a_c = int(dat.rstrip('g'))//2
            else: return
            self.r_w_reg(LSM6DSO_CTRL1_XL, self._scale_a<<2, 0xF3)

    def scale_g(self, dat=None):
        if (dat is None) or (dat == ''):
            return LSM6DSO_SCALEG[self._scale_g]
        else:
            if type(dat) is str:
                if not dat in LSM6DSO_SCALEG: return
                self._scale_g = LSM6DSO_SCALEG.index(dat)
                self._scale_g_c = int(dat)//125
            else: return
            self.r_w_reg(LSM6DSO_CTRL2_G, self._scale_g<<1, 0xF1)

    def power(self, on=None):
        if on is None:
            return self._power
        else:
            self._power = on
            if on:
                self.r_w_reg(LSM6DSO_CTRL1_XL, self._power_a, 0x0F)
                self.r_w_reg(LSM6DSO_CTRL2_G, self._power_g, 0x0F)
            else:
                self._power_a = self.getreg(LSM6DSO_CTRL1_XL) & 0xF0
                self._power_g = self.getreg(LSM6DSO_CTRL2_G) & 0xF0
                self.r_w_reg(LSM6DSO_CTRL1_XL, 0, 0x0F)
                self.r_w_reg(LSM6DSO_CTRL2_G, 0, 0x0F)
