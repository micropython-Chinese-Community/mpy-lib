'''
    mpy drive for I2C LCD1602

    Author: shaoziyang
    Date:   2018.2

    https://www.micropython.org.cn

'''
from time import sleep_ms

LCD_I2C_ADDR=const(63)

class I2C_LCD1602():
    def __init__(self, i2c, addr = 0):
        self.i2c=i2c
        self.buf = bytearray(1)
        self.BK, self.RS, self.E = 0x08, 0x00, 0x04
        self.ADDR = addr if addr else self.autoaddr()
        self.setcmd(0x33)
        sleep_ms(5)
        self.send(0x30)
        sleep_ms(5)
        self.send(0x20)
        sleep_ms(5)
        for i in [0x28, 0x0C, 0x06, 0x01]:
            self.setcmd(i)
        self.px, self.py = 0, 0
        self.pb = bytearray(16)
        self.version='2.1'

    def setReg(self, dat):
        self.buf[0] = dat
        self.i2c.writeto(self.ADDR, self.buf)
        sleep_ms(1)

    def send(self, dat):
        d=(dat&0xF0)|self.BK|self.RS
        self.setReg(d)
        self.setReg(d|0x04)
        self.setReg(d)

    def setcmd(self, cmd):
        self.RS=0
        self.send(cmd)
        self.send(cmd<<4)

    def setdat(self, dat):
        self.RS=1
        self.send(dat)
        self.send(dat<<4)

    def autoaddr(self):
        for i in range(32, 63):
            try:
                if self.i2c.readfrom(i, 1):
                    return i
            except:
                pass
        raise Exception('I2C address detect error!')

    def write_cgram(self, buf, reg=0):
        n = len(buf)
        self.setcmd(0x40 + (reg%8)*8)
        for i in range(n):
            self.setdat(buf[i])

    def clear(self):
        self.setcmd(1)

    def backlight(self, on):
        if on:
            self.BK=0x08
        else:
            self.BK=0
        self.setcmd(0)

    def on(self):
        self.setcmd(0x0C)

    def off(self):
        self.setcmd(0x08)

    def shl(self):
        self.setcmd(0x18)

    def shr(self):
        self.setcmd(0x1C)

    def char(self, ch, x=-1, y=0):
        if x>=0:
            a=0x80
            if y>0:
                a=0xC0
            self.setcmd(a+x)
        self.setdat(ch)

    def puts(self, s, x=0, y=0):
        if type(s) is not str:
            s = str(s)
        if len(s)>0:
            self.char(ord(s[0]),x,y)
            for i in range(1, len(s)):
                self.char(ord(s[i]))

    def newline(self):
        self.px = 0
        if self.py < 1:
            self.py += 1
        else:
            for i in range(16):
                self.char(self.pb[i], i)
                self.char(32, i, 1)
                self.pb[i] = 32

    def print(self, s):
        if type(s) is not str:
            s = str(s)
        for i in range(len(s)):
            d = ord(s[i])
            if d == ord('\n'):
                self.newline()
            else:
                self.char(d, self.px, self.py)
                if self.py:
                    self.pb[self.px] = d
                self.px += 1
                if self.px > 15:
                    self.newline()
