# LSM303AH: ST's ultra-low-power 3D accelerometer and 3D magnetometer micropython drive
# ver: 1.0
# License: MIT
# Author: shaoziyang (shaoziyang@mail.micropython.org.cn)
# v1.0 2019.5

LSM303AH_ADDR_A = const(0x1D)
LSM303AH_ADDR_M = const(0x1E)

LSM303AH_SCALEA = ('2g', '16g', '4g', '8g')
LSM303AH_COEA = (1, 8, 2, 4)

LSM303AH_WHO_AM_I_A = const(0x0F)
LSM303AH_CTRL1_A = const(0x20)
LSM303AH_CTRL2_A = const(0x21)
LSM303AH_CTRL3_A = const(0x22)
LSM303AH_CTRL4_A = const(0x23)
LSM303AH_CTRL5_A = const(0x24)
LSM303AH_FIFO_CTRL_A = const(0x25)
LSM303AH_OUT_T_A = const(0x26)
LSM303AH_STATUS_A = const(0x27)
LSM303AH_OUT_X_L_A = const(0x28)
LSM303AH_OUT_Y_L_A = const(0x2A)
LSM303AH_OUT_Z_L_A = const(0x2C)

LSM303AH_WHO_AM_I_M = const(0x4F)
LSM303AH_CFG_REG_A_M = const(0x60)
LSM303AH_CFG_REG_B_M = const(0x61)
LSM303AH_CFG_REG_C_M = const(0x62)
LSM303AH_INT_CTRL_REG_M = const(0x63)
LSM303AH_INT_SOURCE_REG_M = const(0x64)
LSM303AH_INT_THS_L_REG_M = const(0x65)
LSM303AH_INT_THS_H_REG_M = const(0x66)

LSM303AH_OUTX_L_REG_M = const(0x68)
LSM303AH_OUTY_L_REG_M = const(0x6A)
LSM303AH_OUTZ_L_REG_M = const(0x6C)


class LSM303AH():
    def __init__(self, i2c):
        self.i2c = i2c
        self.tb = bytearray(1)
        self.rb = bytearray(1)
        if self.getreg(LSM303AH_ADDR_A, 15) != 0x43 and self.getreg(LSM303AH_ADDR_M, 79) != 0x40:
            raise Exception('sensor ID error')
        self.irq_v = [[0, 0, 0], [0, 0, 0]]
        self._power = True
        self._power_a = 0x10
        self._power_m = 0x10
        self._scale_a = 0
        self._scale_m = 0
        self._mag_irq = 0
        # soft reset
        self.setreg(LSM303AH_ADDR_A, LSM303AH_CTRL2_A, 0x40)
        self.setreg(LSM303AH_ADDR_M, LSM303AH_CFG_REG_A_M, 0x20)
        # ODR_A=6 FS=0
        self.setreg(LSM303AH_ADDR_A, LSM303AH_CTRL1_A, 0x60)
        # ODR_M=0 MD=0
        self.setreg(LSM303AH_ADDR_M, LSM303AH_CFG_REG_A_M, 0x80)

    def int16(self, d):
        return d if d < 0x8000 else d - 0x10000

    def setreg(self, addr, reg, dat):
        self.tb[0] = dat
        self.i2c.writeto_mem(addr, reg, self.tb)

    def getreg(self, addr, reg):
        self.i2c.readfrom_mem_into(addr, reg, self.rb)
        return self.rb[0]

    def get2reg(self, addr, reg):
        return self.getreg(addr, reg) + self.getreg(addr, reg+1) * 256

    def r_w_reg(self, addr, reg, dat, mask):
        self.getreg(addr, reg)
        self.rb[0] = (self.rb[0] & mask) | dat
        self.setreg(addr, reg, self.rb[0])

    def ax_raw(self):
        return self.int16(self.get2reg(LSM303AH_ADDR_A, LSM303AH_OUT_X_L_A))

    def ay_raw(self):
        return self.int16(self.get2reg(LSM303AH_ADDR_A, LSM303AH_OUT_Y_L_A))

    def az_raw(self):
        return self.int16(self.get2reg(LSM303AH_ADDR_A, LSM303AH_OUT_Z_L_A))

    def a_raw(self):
        self.irq_v[0][0] = self.ax_raw()
        self.irq_v[0][1] = self.ay_raw()
        self.irq_v[0][2] = self.az_raw()
        return self.irq_v[0]

    def convert_a(self, a):
        return LSM303AH_COEA[self._scale_a]*0.061*a

    def ax(self):
        self.convert_a(self.ax_raw())

    def ay(self):
        self.convert_a(self.ay_raw())

    def az(self):
        self.convert_a(self.az_raw())

    def a(self):
        self.irq_v[0][0] = self.ax()
        self.irq_v[0][1] = self.ay()
        self.irq_v[0][2] = self.az()
        return self.irq_v[0]

    def scale_a(self, dat=None):
        if dat is None:
            return LSM303AH_SCALEA[self._scale_a]
        else:
            if type(dat) is str:
                if not dat in LSM303AH_SCALEA: return
                self._scale_a = LSM303AH_SCALEA.index(dat)
            else: return
            self.r_w_reg(LSM303AH_ADDR_A, LSM303AH_CTRL1_A, self._scale_a<<2, 0xF3)

    def mx_raw(self):
        return self.int16(self.get2reg(LSM303AH_ADDR_M, LSM303AH_OUTX_L_REG_M))

    def my_raw(self):
        return self.int16(self.get2reg(LSM303AH_ADDR_M, LSM303AH_OUTY_L_REG_M))

    def mz_raw(self):
        return self.int16(self.get2reg(LSM303AH_ADDR_M, LSM303AH_OUTZ_L_REG_M))

    def m_raw(self):
        self.irq_v[1][0] = self.mx_raw()
        self.irq_v[1][1] = self.my_raw()
        self.irq_v[1][2] = self.mz_raw()
        return self.irq_v[1]

    def mx(self):
        return self.mx_raw()*3//2

    def my(self):
        return self.my_raw()*3//2

    def mz(self):
        return self.mz_raw()*3//2

    def m(self):
        self.irq_v[1][0] = self.mx()
        self.irq_v[1][1] = self.my()
        self.irq_v[1][2] = self.mz()
        return self.irq_v[1]

    def mag_irq(self, on = None, pin = None, callback = None, ths = 0xC0):
        if on == None:
            return self._mag_irq
        elif on == True:
            self._mag_irq = 1
            self.setreg(LSM303AH_ADDR_M, LSM303AH_INT_THS_L_REG_M, ths)
            self.setreg(LSM303AH_ADDR_M, LSM303AH_INT_THS_H_REG_M, ths>>8)
            self.r_w_reg(LSM303AH_ADDR_M, LSM303AH_CFG_REG_C_M, 0x40, 0x3B)
            self.setreg(LSM303AH_ADDR_M, LSM303AH_INT_CTRL_REG_M, 0xE5)
            if pin != None and callback != None:
                pin.init(Pin.IN)
                pin.irq(handler=callback, trigger=Pin.IRQ_RISING)
        else:
            self._mag_irq = 0
            self.setreg(LSM303AH_ADDR_M, LSM303AH_INT_CTRL_REG_M, 0x00)

    def temperature(self):
        self.getreg(LSM303AH_ADDR_A, LSM303AH_OUT_T_A)
        if self.rb[0] > 127: self.rb[0] -= 256
        return self.rb[0] + 25

    def power(self, on=None):
        if on is None:
            return self._power
        else:
            self._power = on
            if on:
                self.r_w_reg(LSM303AH_ADDR_A, LSM303AH_CTRL1_A, self._power_a, 0x0F)
                self.r_w_reg(LSM303AH_ADDR_M, LSM303AH_CFG_REG_A_M, self._power_m, 0xFC)
            else:
                self._power_a = self.getreg(LSM303AH_CTRL1_A) & 0xF0
                self._power_m = self.getreg(LSM303AH_CFG_REG_A_M) & 0x03
                self.r_w_reg(LSM303AH_ADDR_A, LSM303AH_CTRL1_A, 0, 0x0F)
                self.r_w_reg(LSM303AH_ADDR_M, LSM303AH_CFG_REG_A_M, 3, 0x03)

