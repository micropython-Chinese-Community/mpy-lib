'''
    OLED ASCII display drive for micropython.

    Author: shaoziyang
    Date:   2020.1

    https://www.micropython.org.cn

'''
from micropython import const

# register definitions
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_IREF_SELECT = const(0xAD)
SET_COM_OUT_DIR = const(0xC0)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CHARGE_PUMP = const(0x8D)

from Font_6x8 import Font_6x8
from Font_8x16 import Font_8x16
from Font_12x24 import Font_12x24
from Font_16x32 import Font_16x32

Font_6_8 = const(1)
Font_8_16 = const(2)
Font_12_24 = const(3)
Font_16_32 = const(4)

OLED_ADDR = const(0x3C)

class OLED_I2C():
    def __init__(self, i2c, width=128, height=64, ADDR = OLED_ADDR, external_vcc=False):
        self.temp = bytearray(2)
        self.external_vcc = external_vcc
        self.px = 0
        self.py = 0
        self.width = width
        self.height = height
        self.MAX_X = width-1
        self.MAX_Y = height-1
        self.i2c = i2c
        self.screen = bytearray(width*height//8 + 1)
        self.screen[0] = 0x40
        self._DRAW = 1
        self._sav = 0
        self.ADDR = ADDR
        self.Font(1)
        for cmd in (
            SET_DISP,  # display off
            # address setting
            SET_MEM_ADDR,
            0x00,  # horizontal
            # resolution and layout
            SET_DISP_START_LINE,  # start at line 0
            SET_SEG_REMAP | 0x01,  # column addr 127 mapped to SEG0
            SET_MUX_RATIO,
            self.height - 1,
            SET_COM_OUT_DIR | 0x08,  # scan from COM[N] to COM0
            SET_DISP_OFFSET,
            0x00,
            SET_COM_PIN_CFG,
            0x02 if self.width > 2 * self.height else 0x12,
            # timing and driving scheme
            SET_DISP_CLK_DIV,
            0x80,
            SET_PRECHARGE,
            0x22 if self.external_vcc else 0xF1,
            SET_VCOM_DESEL,
            0x30,  # 0.83*Vcc
            # display
            SET_CONTRAST,
            0xFF,  # maximum
            SET_ENTIRE_ON,  # output follows RAM contents
            SET_NORM_INV,  # not inverted
            SET_IREF_SELECT,
            0x30,  # enable internal IREF during display on
            # charge pump
            SET_CHARGE_PUMP,
            0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01,  # display on
        ):  # on
            self.command(cmd)
        self.clear()

    def command(self, cmd):
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.ADDR, self.temp)

    def set_pos(self, col=0, page=0):
        self.command(0xb0 | page)
        c1, c2 = col & 0x0F, col >> 4
        self.command(0x00 | c1)
        self.command(0x10 | c2)

    def pixel(self, x, y, color=1):
        if x<0 or x>self.MAX_X or y<0 or y>self.MAX_Y:
            return
        page, shift_page = divmod(y, 8)
        ind = x + page * 128 + 1
        b = self.screen[ind] | (1 << shift_page) if color else self.screen[ind] & ~ (1 << shift_page)
        self.screen[ind] = b
        if self._DRAW:
            self.set_pos(x, page)
            self.i2c.writeto(self.ADDR, bytearray([0x40, b]))

    def invert(self, v=1):
        n = 0xa7 if v else 0xa6
        self.command(n)

    def on(self, v = 1):
        d = 0xAF if v else 0xAE
        self.command(d)

    def clear(self, c=0):
        for i in range(1, len(self.screen)):
            self.screen[i] = 0
        self.draw()

    def draw(self):
        if self._DRAW:
            self.set_pos()
            self.i2c.writeto(self.ADDR, self.screen)
    
    def zoom(self, z=1):
        self.command(0xD6)
        self.command(1 if z else 0)
        
    def rotate(self, rotate=1):
        self.command(0xC0 | ((rotate & 1) << 3))
        self.command(0xA0 | (rotate & 1))

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
        if self.py > (self.height//8-1):
            self.py = self.height//8-1
            for i in range(1, len(self.screen)-self.width):
                self.screen[i] = self.screen[i+self.width]
            for i in range(self.width):
                self.screen[-i-1] = 0
        self.draw()

    def char_6x8(self, x=0, y=0, ch=32, c=1):
        try:
            ind = x + y * self.width + 1
            n = (min(127, max(ord(ch), 32)) -32)*5
            for i in range(5):
                self.screen[ind+i] = Font_6x8[n+i] if c else Font_6x8[n+i]^0xFF
            self.screen[ind+5] = 0 if c else 0xFF
            self.set_pos(x, y)
            self.i2c.writeto(self.ADDR, b'\x40' + self.screen[ind:ind + 6])
        except:
            return

    def text_6x8(self, x=0, y=0, s='', c=1, wrap=0):
        for i in range(len(s)):
            self.char(x, y, s[i], c)
            x += 6
            if wrap and (x > self.width-6):
                x = 0
                y += 1

    def print(self, s, c = 1, cr = 1):
        if type(s) != str:
            s = str(s)
        for i in range(len(s)):
            self.char_6x8(self.px, self.py, s[i], c)
            self.px += 6
            if self.px > self.width-6:
                self.scroll()
        if cr:
            self.scroll()

    def char_8x16(self, x=0, y=0, ch=32, c=1):
        try:
            ind = x + y * self.width + 1
            n = (min(127, max(ord(ch), 32)) -32)*14
            for j in range(2):
                ind = x + y * self.width + 1
                for i in range(7):
                    self.screen[ind+i] = Font_8x16[n+i] if c else Font_8x16[n+i]^0xFF
                self.screen[ind+7] = 0 if c else 0xFF
                self.set_pos(x, y)
                self.i2c.writeto(self.ADDR, b'\x40' + self.screen[ind:ind + 8])
                y += 1
                n += 7
        except:
            return

    def text_8x16(self, x=0, y=0, s='', c=1, wrap=0):
        for i in range(len(s)):
            self.char_8x16(x, y, s[i], c)
            x += 8
            if wrap and (x > self.width-8):
                x = 0
                y += 2

    def char_12x24(self, x=0, y=0, ch=32, c=1):
        try:
            n = (min(127, max(ord(ch), 32)) -32)*36
            for j in range(3):
                ind = x + y * self.width + 1
                for i in range(12):
                    self.screen[ind+i] = Font_12x24[n+i] if c else Font_12x24[n+i]^0xFF
                self.set_pos(x, y)
                self.i2c.writeto(self.ADDR, b'\x40' + self.screen[ind:ind + 12])
                y += 1
                n += 12
        except:
            return

    def text_12x24(self, x=0, y=0, s='', c=1, wrap=0):
        for i in range(len(s)):
            self.char_12x24(x, y, s[i], c)
            x += 12
            if wrap and (x > self.width-12):
                x = 0
                y += 3

    def char_16x32(self, x=0, y=0, ch=32, c=1):
        try:
            n = (min(127, max(ord(ch), 32)) -32)*64
            for j in range(4):
                ind = x + y * self.width + 1
                for i in range(16):
                    self.screen[ind+i] = Font_16x32[n+i] if c else Font_16x32[n+i]^0xFF
                self.set_pos(x, y)
                self.i2c.writeto(self.ADDR, b'\x40' + self.screen[ind:ind + 16])
                y += 1
                n += 16
        except:
            return

    def text_16x32(self, x=0, y=0, s='', c=1, wrap=0):
        for i in range(len(s)):
            self.char_16x32(x, y, s[i], c)
            x += 16
            if wrap and (x > self.width-16):
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
