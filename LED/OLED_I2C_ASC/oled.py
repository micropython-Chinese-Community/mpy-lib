'''
    OLED ASCII display drive for micropython.

    Author: shaoziyang
    Date:   2020.1

    https://www.micropython.org.cn

'''

cmd = [
  [0xAE],
  [0xA4],
  [0xD5, 0xF0],
  [0xA8, 0x3F],
  [0xD3, 0x00],
  [0 | 0x0],
  [0x8D, 0x14],
  [0x20, 0x00],
  [0x21, 0, 127],
  [0x22, 0, 63],
  [0xa0 | 0x1],
  [0xc8],
  [0xDA, 0x12],
  [0x81, 0xCF],
  [0xd9, 0xF1],
  [0xDB, 0x40],
  [0xA6],
  [0xd6, 0],
  [0xaf]
]

from Font_6x8 import Font_6x8
from Font_8x16 import Font_8x16
from Font_12x24 import Font_12x24
from Font_16x32 import Font_16x32

Font_6_8 = const(1)
Font_8_16 = const(2)
Font_12_24 = const(3)
Font_16_32 = const(4)

OLED_ADDR = 0x3C
screen = bytearray(1025)
screen[0] = 0x40

class OLED12864_I2C():
    def __init__(self, i2c, ADDR = OLED_ADDR):
        self.px = 0
        self.py = 0
        self.width = 128
        self.height = 64
        self.MAX_X = 127
        self.MAX_Y = 63
        self.i2c = i2c
        self._DRAW = 1
        self._sav = 0
        self.ADDR = ADDR
        self.Font(1)
        for c in cmd:
            self.command(c)
        self.clear()

    def command(self, c):
        self.i2c.writeto(self.ADDR, b'\x00' + bytearray(c))

    def set_pos(self, col=0, page=0):
        self.command([0xb0 | page])
        c1, c2 = col & 0x0F, col >> 4
        self.command([0x00 | c1])
        self.command([0x10 | c2])

    def pixel(self, x, y, color=1):
        if x<0 or x>self.MAX_X or y<0 or y>self.MAX_Y:
            return
        page, shift_page = divmod(y, 8)
        ind = x + page * 128 + 1
        b = screen[ind] | (1 << shift_page) if color else screen[ind] & ~ (1 << shift_page)
        screen[ind] = b
        if self._DRAW:
            self.set_pos(x, page)
            self.i2c.writeto(self.ADDR, bytearray([0x40, b]))

    def invert(self, v=1):
        n = 0xa7 if v else 0xa6
        self.command([n])

    def on(self, v = 1):
        d = 0xAF if v else 0xAE
        self.command([d])

    def clear(self, c=0):
        for i in range(1, 1025):
            screen[i] = 0
        self.draw()

    def draw(self):
        if self._DRAW:
            self.set_pos()
            self.i2c.writeto(self.ADDR, screen)

    def line(self, x1, y1, x2, y2, c=1):
        return

    def hline(self, x, y, len, c=1):
        self._sav = self._DRAW
        self._DRAW = 0

        for i in range(x, min(x+len, self.MAX_X)):
            self.pixel(i, y, c)

        self._DRAW = self._sav
        self.draw()

    def vline(self, x, y, len, c=1):
        self._sav = self._DRAW
        self._DRAW = 0

        for i in range(y, min(y+len, self.MAX_Y)):
            self.pixel(x, i, c)

        self._DRAW = self._sav
        self.draw()

    def rect(self, x1, y1, x2, y2, c=1):
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        self._DRAW = 0
        self.hline(x1, y1, x2 - x1 + 1, c)
        self.hline(x1, y2, x2 - x1 + 1, c)
        self.vline(x1, y1, y2 - y1 + 1, c)
        self.vline(x2, y1, y2 - y1 + 1, c)
        self._DRAW = 1
        self.draw()

    def font(self, FONT):
        self.FONT = FONT

    def scroll(self):
        self.px = 0
        self.py += 1
        if self.py > 7:
            self.py = 7
            for i in range(1, 897):
                screen[i] = screen[i+128]
            for i in range(128):
                screen[-i-1] = 0
        self.draw()

    def char_6x8(self, x=0, y=0, ch=32, c=1):
        try:
            ind = x + y * 128 + 1
            n = (min(127, max(ord(ch), 32)) -32)*5
            for i in range(5):
                screen[ind+i] = Font_6x8[n+i] if c else Font_6x8[n+i]^0xFF
            screen[ind+5] = 0 if c else 0xFF
            self.set_pos(x, y)
            self.i2c.writeto(self.ADDR, b'\x40' + screen[ind:ind + 6])
        except:
            return

    def text_6x8(self, x=0, y=0, s='', c=1, wrap=0):
        for i in range(len(s)):
            self.char(x, y, s[i], c)
            x += 6
            if wrap and x > 120:
                x = 0
                y += 1

    def print(self, s, c = 1, cr = 1):
        for i in range(len(s)):
            self.char_6x8(self.px, self.py, s[i], c)
            self.px += 6
            if self.px > 120:
                self.scroll()
        if cr:
            self.scroll()

    def char_8x16(self, x=0, y=0, ch=32, c=1):
        try:
            ind = x + y * 128 + 1
            n = (min(127, max(ord(ch), 32)) -32)*14
            for j in range(2):
                ind = x + y * 128 + 1
                for i in range(7):
                    screen[ind+i] = Font_8x16[n+i] if c else Font_8x16[n+i]^0xFF
                screen[ind+7] = 0 if c else 0xFF
                self.set_pos(x, y)
                self.i2c.writeto(self.ADDR, b'\x40' + screen[ind:ind + 8])
                y += 1
                n += 7
        except:
            return

    def text_8x16(self, x=0, y=0, s='', c=1, wrap=0):
        for i in range(len(s)):
            self.char_8x16(x, y, s[i], c)
            x += 8
            if wrap and x > 120:
                x = 0
                y += 2

    def char_12x24(self, x=0, y=0, ch=32, c=1):
        try:
            n = (min(127, max(ord(ch), 32)) -32)*36
            for j in range(3):
                ind = x + y * 128 + 1
                for i in range(12):
                    screen[ind+i] = Font_12x24[n+i] if c else Font_12x24[n+i]^0xFF
                self.set_pos(x, y)
                self.i2c.writeto(self.ADDR, b'\x40' + screen[ind:ind + 12])
                y += 1
                n += 12
        except:
            return

    def text_12x24(self, x=0, y=0, s='', c=1, wrap=0):
        for i in range(len(s)):
            self.char_12x24(x, y, s[i], c)
            x += 12
            if wrap and x > 116:
                x = 0
                y += 3

    def char_16x32(self, x=0, y=0, ch=32, c=1):
        try:
            n = (min(127, max(ord(ch), 32)) -32)*64
            for j in range(4):
                ind = x + y * 128 + 1
                for i in range(16):
                    screen[ind+i] = Font_16x32[n+i] if c else Font_16x32[n+i]^0xFF
                self.set_pos(x, y)
                self.i2c.writeto(self.ADDR, b'\x40' + screen[ind:ind + 16])
                y += 1
                n += 16
        except:
            return

    def text_16x32(self, x=0, y=0, s='', c=1, wrap=0):
        for i in range(len(s)):
            self.char_16x32(x, y, s[i], c)
            x += 16
            if wrap and x > 112:
                x = 0
                y += 4

    def Font(self, Font):
        if Font == Font_8_16 or Font == 'Font_8x16':
            self.char = self.char_8x16
            self.text = self.text_8x16
        elif Font == Font_12_24 or Font == 'Font_12x24':
            self.char = self.char_12x24
            self.text = self.text_12x24
        elif Font == Font_16_32 or Font == 'Font_16x32':
            self.char = self.char_16x32
            self.text = self.text_16x32
        else:
            self.char = self.char_6x8
            self.text = self.text_6x8
