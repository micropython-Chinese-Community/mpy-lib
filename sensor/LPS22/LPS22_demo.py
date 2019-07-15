from machine import I2C
import LPS22

i2c = I2C(1)
lps = LPS22.LPS22(i2c)
lps.get()

