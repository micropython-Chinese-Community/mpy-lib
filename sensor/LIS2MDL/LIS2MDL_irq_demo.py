from machine import I2C
from pyb import Timer
import LIS2MDL

i2c = I2C(1)
mdl = LIS2MDL.LIS2MDL(i2c)

def tim_irq(t):
    print(mdl.get())

tim = Timer(1, freq = 1)
tim.callback(tim_irq)
