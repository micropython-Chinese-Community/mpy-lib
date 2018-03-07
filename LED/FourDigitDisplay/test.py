'''
    Four Digit Display demo

    Author: shaoziyang
    Date:   2018.3

    http://www.micropython.org.cn

'''
import machine
import time
import FourDigitDisplay

i2c = machine.I2C(1)
fdd = FourDigitDisplay.FourDigitDisplay(i2c)

n = 0
while 1:
    fdd.shownum(n)
    n += 1
    time.sleep_ms(1000)
