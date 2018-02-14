"""
    ESP8266/ESP32 neopixel 16x16 image display drive

    Author: shaoziyang
    Date:   2018.2

    http://www.micropython.org.cn

"""
from machine import Pin
import neopixel

class neo16x16_img:
    def __init__(self, pin):
        self.np = neopixel.NeoPixel(pin, 256)
    
    def clear(self):
        self.np.fill((0,0,0))
        self.np.write()

    def set(self, n, color):
        self.np[n] = color
        self.np.write()

    def show(self, dat, pos=0):
        for x in range(16):
            for y in range(16):
                if ((x+pos)*16)>=len(dat):
                    self.np[x*16+y]=(0,0,0)
                else:
                    t = dat[(x+pos)*16+y]
                    r=t%256
                    g=(t>>8)%256
                    b=(t>>16)%256
                    if pos%2:
                        self.np[x*16+y] = (r,g,b) 
                    else:
                        self.np[x*16+15-y] = (r,g,b)

        self.np.write()

