'''
    APDS9930 Proximity demo

    Author: shaoziyang
    Date:   2018.4

    http://www.micropython.org.cn

'''
from machine import Pin, I2C
import time
import APDS9930

i2c=I2C(sda=Pin(5),scl=Pin(4))

apds = APDS9930.APDS9930(i2c)
apds.Proximity_Enable()

while True:
    time.sleep_ms(500)
    apds.getProximity()
