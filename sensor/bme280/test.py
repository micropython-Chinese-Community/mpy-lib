'''
    BME280 demo

    Author: shaoziyang
    Date:   2018.2

    http://www.micropython.org.cn

'''
from machine import I2C
import time

import bme280

b = bme280.BME280(I2C(1))

while True:
    time.sleep_ms(500)
    print(b.get())
