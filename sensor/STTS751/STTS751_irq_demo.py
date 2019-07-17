from machine import I2C
from pyb import Timer
import STTS751

i2c = I2C(1)
stt = STTS751.STTS751(i2c)

def tim_irq(t):
    print(stt.temperature_irq())

tim = Timer(1, freq = 1)
tim.callback(tim_irq)
