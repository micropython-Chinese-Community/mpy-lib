from machine import I2C, Pin
from oled import OLED12864_I2C

i2c = I2C(-1, scl = Pin(27, pull = Pin.PULL_UP), sda = Pin(13, pull = Pin.PULL_UP))

oled = OLED12864_I2C(i2c)
oled.text(0, 0, '0123456789')
oled.Font('Font_8x16')
oled.text(0, 1, '0123456789')
oled.Font('Font_12x24')
oled.text(0, 3, '0123456789')
