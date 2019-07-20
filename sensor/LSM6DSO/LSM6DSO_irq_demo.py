from machine import I2C
from pyb import Timer
import LSM6DSO

i2c = I2C(1)
lsm = LSM6DSO.LSM6DSO(i2c)
lsm.ax()
lsm.get_a()
lsm.get()

def tim_irq(t):
    print(lsm.get(), lsm.temperature())

tim = Timer(1, freq = 1)
tim.callback(tim_irq)
