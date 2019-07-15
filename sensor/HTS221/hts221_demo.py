from machine import I2C
import HTS221

i2c = I2C(1)
hts = HTS221.HTS221(i2c)
hts.get()

