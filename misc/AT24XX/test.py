'''
    AT24C32 demo

    Author: shaoziyang
    Date:   2018.3

    http://www.micropython.org.cn
'''
from machine import I2C, Pin
import AT24XX

i2c = I2C(sda = Pin(5), scl=Pin(4))
ee = AT24XX.AT24XX(i2c)

ee.write_byte(0, 12)
ee.read_byte(0)

ee.write_word(4, 0x1234)
ee.read_word(4)

ee.write_buf(800, 'Hello!')
ee.read_buf(800, 8)

