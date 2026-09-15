from time import sleep_ms
from machine import Pin

class LCD1602_595:

    def __init__(self, spi=None, ST_CP=None, SH_CP=None, DS=None):
        self.spi = spi
        self.stcp = ST_CP
        self.stcp.init(Pin.OUT)
        self.stcp(0)
        if self.spi is None:
            self.shcp = SH_CP
            self.shcp.init(Pin.OUT)
            self.shcp(0)
            self.ds = DS
            self.ds.init(Pin.OUT)
        self.RS = 2
        self.E = 4
        self.BK = 8
        self.spibuf = bytearray(1)

        for i in [0x33, 0x32, 0x28, 0x0C, 0x06, 0x01]:
            self.setcmd(i)
            sleep_ms(5)
        self.px, self.py = 0, 0
        self.pb = bytearray(' '*16, '')

    def _send(self, dat):
        self.stcp(0)
        if self.spi is None:
            for i in range(8):
                self.ds(dat&0x80)
                self.shcp(1)
                dat *= 2
                self.shcp(0)
        else:
            self.spibuf[0] = dat
            self.spi.write(self.spibuf)
        self.stcp(1)
        sleep_ms(1)

    def send(self, dat):
        d = (dat&0xF0)|self.RS|self.BK
        self._send(d|0x04)
        self._send(d)

    def setcmd(self, cmd):
        self.RS=0
        self.send(cmd)
        self.send(cmd<<4)

    def setdat(self, dat):
        self.RS=2
        self.send(dat)
        self.send(dat<<4)

    def write_cgram(self, buf, reg=0):
        n = len(buf)
        self.setcmd(0x40 + (reg%8)*8)
        for i in range(n):
            self.setdat(buf[i])

    def clear(self):
        self.setcmd(1)
        self.px = 0
        self.py = 0
        self.pb[:] = b' '*16

    def backlight(self, on=1):
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
        self.py += 1

    def print(self, s, end='\n'):
        if type(s) is not str:
            s = str(s)
        s = s + end
        for i in range(len(s)):
            d = ord(s[i])
            if d == ord('\n'):
                self.newline()
            elif d == ord('\r'):
                self.px = 0
            else:
                if self.py > 1:
                    self.clear()
                    self.py = 1
                    for j in range(16):
                        self.char(self.pb[j], j)
                        self.pb[j] = 32

                self.char(d, self.px, self.py)
                if self.py:
                    self.pb[self.px] = d
                self.px += 1
                if self.px > 15:
                    self.newline()
