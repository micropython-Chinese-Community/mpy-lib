from machine import I2C
import LIS2MDL

i2c = I2C(1)
mdl = LIS2MDL.LIS2MDL(i2c)
mdl.x()
mdl.get()
