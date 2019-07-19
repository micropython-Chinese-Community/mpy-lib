from machine import I2C
import LIS2DW12

i2c = I2C(1)
lis = LIS2DW12.LIS2DW12(i2c)
lis.x()
lis.get()
