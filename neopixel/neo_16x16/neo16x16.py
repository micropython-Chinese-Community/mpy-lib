"""
    ESP8266/ESP32 neopixel 16x16 display drive

    Author: shaoziyang
    Date:   2018.2

    http://www.micropython.org.cn

"""
from machine import Pin
import neopixel

class neo16x16:
    def __init__(self, pin):
        self.np = neopixel.NeoPixel(pin, 256)
        self.color = (0,0,8)
    
    def clear(self):
        self.np.fill((0,0,0))
        self.np.write()

    def set(self, n, color=''):
        if color!='':
            self.np[n] = color
        else:
            self.np[n] = self.color
        self.np.write()

    def setcolor(self, color):
        self.color = color

    def show(self, dat, offset=0, clear = True, color=''):
        if color != '':
            self.color = color
        if clear:
            self.np.fill((0,0,0))
        for x in range(16):
            for y in range(16):
                if (x+offset)>=len(dat):
                    self.np[x*16+y]=(0,0,0)
                else:
                    if (1<<y)&dat[x+offset]:
                        if offset%2==0:
                            self.np[x*16 + y] = self.color
                        else:
                            self.np[x*16 +15 - y] = self.color

        self.np.write()

