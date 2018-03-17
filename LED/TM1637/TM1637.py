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

_SEGMENTS = (0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F,0x77,0x7C,0x39,0x5E,0x79,0x71)

class TM1637():
    def __init__(self, clk, dio, intensity=7, number = 4):
        self.clk = clk
        self.dio = dio

        self._intensity = intensity%8
        self._LED = number
        self._ON = 8
        self.dbuf = [0, 0, 0, 0]

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

    def _dat(self, bit, dat):
        self._write_data_cmd()
        self._start()
        self._write_byte(TM1637_CMD2 | (bit%self._LED))
        self._write_byte(dat)
        self._stop()
        self._write_dsp_ctrl()

    def clear(self):
        self._dat(0, 0)
        self._dat(1, 0)
        self._dat(2, 0)
        self._dat(3, 0)
        self.dbuf = [0, 0, 0, 0]

    def showbit(self, num, bit = 0):
        self.dbuf[bit%self._LED] = _SEGMENTS[num%16]
        self._dat(bit, _SEGMENTS[num%16])

    def showDP(self, bit = 1, show = True):
        bit = bit%self._LED
        if show:
            self._dat(bit, self.dbuf[bit] | 0x80)
        else:
            self._dat(bit, self.dbuf[bit] & 0x7F)

    def shownum(self, num):
        if num < 0:
            self._dat(0, 0x40)   # '-'
            num = -num
        else:
            self.showbit((num // 1000) % 10)
        self.showbit(num % 10, 3)
        self.showbit((num // 10) % 10, 2)
        self.showbit((num // 100) % 10, 1)

    def showhex(self, num):
        if num < 0:
            self._dat(0, 0x40)   # '-'
            num = -num
        else:
            self.showbit((num >> 12) % 16)
        self.showbit(num % 16, 3)
        self.showbit((num >> 4) % 16, 2)
        self.showbit((num >> 8) % 16, 1)


