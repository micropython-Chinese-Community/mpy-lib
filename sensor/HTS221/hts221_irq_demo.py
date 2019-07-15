from machine import I2C
import HTS221
from pyb import Timer

i2c = I2C(1)
hts = HTS221.HTS221(i2c)

def tim_irq(t):
    print(hts.get_irq())

tim = Timer(1, freq = 1)
tim.callback(tim_irq)
