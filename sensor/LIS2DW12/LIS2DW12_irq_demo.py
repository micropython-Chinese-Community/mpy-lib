from machine import I2C
from pyb import Timer
import LIS2DW12

i2c = I2C(1)
lis = LIS2DW12.LIS2DW12(i2c)
lis.x()

def tim_irq(t):
    print(lis.get())

tim = Timer(1, freq = 1)
tim.callback(tim_irq)
