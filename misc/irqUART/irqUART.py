'''
    UART with rx irq

    Author: shaoziyang
    Date:   2020.6

    http://www.micropython.org.cn
'''
from machine import Pin, UART, Timer
import sys

class irqUART():
    # uart: uart object
    # rx_pin: uart rxd pin
    # rx_irq: user rxd irq
    # frame_irq: user frame irq
    # CHR_TMO: rxd irq delay (ms) after rx_pin irq
    # FRAME_TMO: frame irq delay (ms) after last char
    def __init__(self, uart, rx_pin, rx_irq=None, frame_irq=None, CHR_TMO=3, FRAME_TMO=100):
        self._rxpin = rx_pin
        self._rxirq = rx_irq
        self._frameirq = frame_irq
        self._CHR_TMO = CHR_TMO
        self._FRAME_TMO = FRAME_TMO
        self._rxpin.init(Pin.IN)
        self._rxpin.irq(trigger = Pin.IRQ_FALLING, handler = self._RXPIN_IRQ)
        self._TMRX = Timer(-1)
        self._TMRX_sta = 0
        self._mode = Timer.ONE_SHOT if sys.platform == 'pyboard' else Timer.PERIODIC
        self.uart = uart

    def _RXPIN_IRQ(self, t):
        if self._TMRX_sta == 0:
            self._TMRX_sta = 1
            self._TMRX.deinit()
            self._TMRX.init(period = self._CHR_TMO, mode = self._mode, callback = self._TMRX_IRQ)

    def _TMRX_IRQ(self, t):
        if self._TMRX_sta != 0:
            if self._frameirq != None and self._FRAME_TMO > 0:
                self._TMRX.deinit()
                self._TMRX.init(period = self._FRAME_TMO, mode = Timer.ONE_SHOT, callback = self._TMRX_IRQ)
            if self._rxirq != None:
                self._rxirq(0)
        else:
            if self._frameirq != None:
                self._frameirq(0)
        self._TMRX_sta = 0

