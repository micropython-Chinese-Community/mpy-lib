'''
    mpy drive for Four Digit LED Display (TM1637)

    Author: shaoziyang
    Date:   2018.3

    http://www.micropython.org.cn

'''
from machine import Pin
from time import sleep_us

TM1637_CMD1 = (64)  # 0x40 data command
TM1637_CMD2 = (192) # 0xC0 address command
TM1637_CMD3 = (128) # 0x80 display control command
TM1637_DELAY = (10) # 10us delay between clk/dio pulses


'''
0x00-0x0F
0x10-0x1F
0x20-0x2F
0x30-0x39 0 ~ 9
0x3A-0x40
0x41-0x5A A - Z
0x5B-0x60
'''
_FONT1 = b'\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\
\x3F\x06\x5B\x4F\x66\x6D\x7D\x07\x7F\x6F\
\x00\x00\x00\x00\x00\x00\x00\
\x77\x7C\x39\x5E\x79\x71\x3D\x76\x00\x0E\x00\x38\x00\x54\x5C\x73\x67\x00\x00\x78\x3E\x1C\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x08\x00\
'
_FONT2 = b'\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\
\x3F\x30\x5B\x79\x74\x6D\x6F\x38\x7F\x7D\
\x00\x00\x00\x00\x00\x00\x00\
\x7E\x67\x0F\x73\x4F\x4E\x2F\x76\x00\x31\x00\x07\x00\x62\x63\x5E\x7C\x00\x00\x47\x37\x23\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x01\x00\
'

class TM1637():
    def __init__(self, clk, dio, intensity=7, number = 4):
        self.clk = clk
        self.dio = dio

        self._intensity = intensity%8
        self._LEDS = number
        self._ON = 8
        self.dbuf = [0]*number
        self._reverse = False
        self.FONT = _FONT1

        self.clk.init(Pin.OUT, value=0)
        self.dio.init(Pin.OUT, value=0)
        sleep_us(TM1637_DELAY)

        self.clear()

    def _start(self):
        self.dio(0)
        sleep_us(TM1637_DELAY)
        self.clk(0)
        sleep_us(TM1637_DELAY)

    def _stop(self):
        self.dio(0)
        sleep_us(TM1637_DELAY)
        self.clk(1)
        sleep_us(TM1637_DELAY)
        self.dio(1)

    def _write_data_cmd(self):
        # automatic address increment, normal mode
        self._start()
        self._write_byte(TM1637_CMD1)
        self._stop()

    def _write_dsp_ctrl(self):
        # display on, set brightness
        self._start()
        self._write_byte(TM1637_CMD3 | self._ON | self._intensity)
        self._stop()

    def _write_byte(self, b):
        for i in range(8):
            self.dio((b >> i) & 1)
            sleep_us(TM1637_DELAY)
            self.clk(1)
            sleep_us(TM1637_DELAY)
            self.clk(0)
            sleep_us(TM1637_DELAY)
        self.clk(1)
        sleep_us(TM1637_DELAY)
        self.clk(0)
        sleep_us(TM1637_DELAY)

    def on(self):
        self._ON = 8
        self._write_data_cmd()
        self._write_dsp_ctrl()

    def off(self):
        self._ON = 0
        self._write_data_cmd()
        self._write_dsp_ctrl()

    def intensity(self, val=None):
        if val is None:
            return self._intensity
        val = max(0, min(val, 8))
        if val == 0:
            self.off()
        else:
            self._ON = 8
            self._intensity = val-1
            self._write_data_cmd()
            self._write_dsp_ctrl()

    def reverse(self, reverse=False):
        self._reverse = reverse
        if reverse:
            self.FONT = _FONT2
        else:
            self.FONT = _FONT1
        
    def dat(self, dat, bit=0):
        if self._reverse:
            bit = self._LEDS - bit - 1
        self._write_data_cmd()
        self._start()
        self._write_byte(TM1637_CMD2 | (bit%self._LEDS))
        self._write_byte(dat)
        self._stop()
        self._write_dsp_ctrl()

    def clear(self):
        for i in range(self._LEDS):
            self.dat(0, i)
            self.dbuf[i] = 0

    def showDP(self, show = True, bit = 1):
        bit = bit%self._LEDS
        if show:
            self.dat(self.dbuf[bit] | 0x80, bit)
        else:
            self.dat(self.dbuf[bit] & 0x7F, bit)

    def show(self, s):
        _s = s.upper()
        for i in range(self._LEDS):
            if i < len(_s):
                self.dbuf[i] = self.FONT[min(0x60, ord(_s[i]))]
            else:
                self.dbuf[i] = 0
            self.dat(self.dbuf[i], i)

    def shownum(self, num):
        self.show(str(num))


