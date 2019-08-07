'''
    I2C LCD1602 demo

    Author: shaoziyang
    Date:   2018.2

    http://www.micropython.org.cn

'''
from machine import I2C
import time

l = LCD1602(I2C(1))
l.puts("Hello microbit!")
n = 0
while 1:
    l.puts(str(n), 0, 1)
    n = n + 1
    time.sleep_ms(1000)

