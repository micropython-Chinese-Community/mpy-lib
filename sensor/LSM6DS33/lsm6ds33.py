# LSM6DS33: ST's always-on 3D accelerometer and 3D gyroscope micropython drive
# ver: 1.0
# License: MIT
# Author: shaoziyang (shaoziyang@mail.micropython.org.cn)
# v1.0 2019.5

LSM6DS33_ORIENT_CFG_G = const(0x0B)
LSM6DS33_INT1_CTRL = const(0x0D)
LSM6DS33_INT2_CTRL = const(0x0E)
LSM6DS33_CTRL1_XL = const(0x10)
LSM6DS33_CTRL2_G = const(0x11)
LSM6DS33_CTRL3_C = const(0x12)
LSM6DS33_CTRL4_C = const(0x13)
LSM6DS33_CTRL5_C = const(0x14)
LSM6DS33_CTRL6_C = const(0x15)
LSM6DS33_CTRL7_G = const(0x16)
LSM6DS33_CTRL8_XL = const(0x17)
LSM6DS33_CTRL9_XL = const(0x18)
LSM6DS33_CTRL10_C = const(0x19)
LSM6DS33_WAKE_UP_SRC = const(0x1B)
LSM6DS33_STATUS = const(0x1E)
LSM6DS33_OUT_TEMP_L = const(0x20)
LSM6DS33_OUTX_L_G = const(0x22)
LSM6DS33_OUTY_L_G = const(0x24)
LSM6DS33_OUTZ_L_G = const(0x26)
LSM6DS33_OUTX_L_XL = const(0x28)
LSM6DS33_OUTY_L_XL = const(0x2A)
LSM6DS33_OUTZ_L_XL = const(0x2C)
LSM6DS33_TAP_CFG = const(0x58)
LSM6DS33_WAKE_UP_THS = const(0x5B)
LSM6DS33_WAKE_UP_DUR = const(0x5C)
LSM6DS33_MD1_CFG = const(0x5E)
LSM6DS33_MD2_CFG = const(0x5F)

LSM6DS33_SCALEA = ('2g', '16g', '4g', '8g')
LSM6DS33_COEA = (1, 8, 2, 4)
LSM6DS33_SCALEG = ('250', '125', '500', '', '1000', '', '2000')
LSM6DS33_COEG = (2, 1, 4, 0, 8, 0, 16)

class LSM6DS33():
    def __init__(self, i2c, addr = 0x6B):
        self.i2c = i2c
        self.addr = addr
        self.tb = bytearray(1)
        self.rb = bytearray(1)
        self.irq_v = [[0, 0, 0], [0, 0, 0]]
        self._power = True
        self._power_a = 0x10
        self._power_g = 0x10
        self._wakeup_mode = 0
        if self.getreg(15) != 0x69:
            raise Exception('sensor ID error')
        # RESET
        self.setreg(LSM6DS33_CTRL3_C, 1)
        # ODR_XL=6 FS_XL=0
        self.setreg(LSM6DS33_CTRL1_XL, 0x60)
        # ODR_G=4 FS=250
        self.setreg(LSM6DS33_CTRL2_G, 0x40)
        # BDU=1 IF_INC=1
        self.setreg(LSM6DS33_CTRL3_C, 0x44)
        self.setreg(LSM6DS33_CTRL8_XL, 0)
        # scale=2G 125dps
        self._scale_a = 0
        self._scale_g = 0

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
        return self.int16(self.get2reg(LSM6DS33_OUTX_L_XL))

    def ay_raw(self):
        return self.int16(self.get2reg(LSM6DS33_OUTY_L_XL))

    def az_raw(self):
        return self.int16(self.get2reg(LSM6DS33_OUTZ_L_XL))

    def gx_raw(self):
        return self.int16(self.get2reg(LSM6DS33_OUTX_L_G))

    def gy_raw(self):
        return self.int16(self.get2reg(LSM6DS33_OUTY_L_G))

    def gz_raw(self):
        return self.int16(self.get2reg(LSM6DS33_OUTZ_L_G))

    def a_raw(self):
        self.irq_v[0][0] = self.ax_raw()
        self.irq_v[0][1] = self.ay_raw()
        self.irq_v[0][2] = self.az_raw()
        return self.irq_v[0]

    def g_raw(self):
        self.irq_v[1][0] = self.gx_raw()
        self.irq_v[1][1] = self.gy_raw()
        self.irq_v[1][2] = self.gz_raw()
        return self.irq_v[1]

    def t_raw(self):
        return self.get2reg(LSM6DS33_OUT_TEMP_L)

    def temperature(self):
        try:
            return self.int16(self.t_raw())/16 + 25
        except MemoryError:
            return self.int16(self.t_raw())//16 + 25

    def scale_a(self, dat=None):
        if dat is None:
            return LSM6DS33_SCALEA[self._scale_a]
        else:
            if type(dat) is str:
                if not dat in LSM6DS33_SCALEA: return
                self._scale_a = LSM6DS33_SCALEA.index(dat)
            else: return
            self.r_w_reg(LSM6DS33_CTRL1_XL, self._scale_a<<2, 0xF3)

    def scale_g(self, dat=None):
        if (dat is None) or (dat == ''):
            return LSM6DS33_SCALEG[self._scale_g]
        else:
            if type(dat) is str:
                if not dat in LSM6DS33_SCALEG: return
                self._scale_g = LSM6DS33_SCALEG.index(dat)
            else: return
            self.r_w_reg(LSM6DS33_CTRL2_G, self._scale_g<<1, 0xF1)

    def wakeup_mode(self, on = None, pin = None, callback = None, ths = 0x20):
        if on == None:
            return self._wakeup_mode
        if on == True:
            self._wakeup_mode = 1
            # ENABLE SLOPE_FDS
            self.r_w_reg(LSM6DS33_TAP_CFG, 0x10, 0xEF)
            # WAKE_UP_THS = 20
            self.setreg(LSM6DS33_WAKE_UP_THS, ths)
            # INT1_WU=1
            self.r_w_reg(LSM6DS33_MD1_CFG, 0x20, 0xDF)
            if pin != None and callback != None:
                pin.init(Pin.IN)
                pin.irq(handler=callback, trigger=Pin.IRQ_RISING)
        else:
            self._wakeup_mode = 0
            self.r_w_reg(LSM6DS33_TAP_CFG, 0x00, 0xEF)
            self.r_w_reg(LSM6DS33_MD1_CFG, 0x00, 0xDF)

    def power(self, on=None):
        if on is None:
            return self._power
        else:
            self._power = on
            if on:
                self.r_w_reg(LSM6DS33_CTRL1_XL, self._power_a, 0x0F)
                self.r_w_reg(LSM6DS33_CTRL2_G, self._power_g, 0x0F)
            else:
                self._power_a = self.getreg(LSM6DS33_CTRL1_XL) & 0xF0
                self._power_g = self.getreg(LSM6DS33_CTRL2_G) & 0xF0
                self.r_w_reg(LSM6DS33_CTRL1_XL, 0, 0x0F)
                self.r_w_reg(LSM6DS33_CTRL2_G, 0, 0x0F)

    def convert_a(self, a):
        return LSM6DS33_COEA[self._scale_a]*0.061*a

    def convert_g(self, g):
        return LSM6DS33_COEG[self._scale_g]*4.375*g

    def ax(self):
        self.convert_a(self.ax_raw())

    def ay(self):
        self.convert_a(self.ay_raw())

    def az(self):
        self.convert_a(self.az_raw())

    def gx(self):
        self.convert_g(self.gx_raw())

    def gy(self):
        self.convert_g(self.gy_raw())

    def gz(self):
        self.convert_g(self.gz_raw())

    def a(self):
        self.irq_v[0][0] = self.ax()
        self.irq_v[0][1] = self.ay()
        self.irq_v[0][2] = self.az()
        return self.irq_v[0]

    def g(self):
        self.irq_v[1][0] = self.gx()
        self.irq_v[1][1] = self.gy()
        self.irq_v[1][2] = self.gz()
        return self.irq_v[1]
