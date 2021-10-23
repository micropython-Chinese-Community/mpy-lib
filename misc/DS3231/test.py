'''
    DS3231 demo

    Author: shaoziyang
    Date:   2018.3

    http://www.micropython.org.cn
'''
from machine import I2C, Pin
import DS3231

i2c = I2C(sda = Pin(5), scl=Pin(4))
ds = DS3231.DS3231(i2c)

ds.Hour(12)

ds.Time()
ds.Time([12,10,0])

ds.DateTime([2018,3,12,1,22,10,0])

ds.ALARM(12, 20, 10, DS3231.PER_DISABLE)
ds.ALARM(12, 20, 10, DS3231.PER_DAY)
ds.ClearALARM()
