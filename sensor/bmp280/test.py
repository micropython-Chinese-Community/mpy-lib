'''
    BMP280 demo

    Author: shaoziyang
    Date:   2018.2

    https://github.com/shaoziyang

'''
from machine import I2C
import time

import bmp280

b = bmp280.BMP280(I2C(1))

while True:
    time.sleep_ms(500)
    b.get()
