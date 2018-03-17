'''
    Four Digit Display (TM1637) demo

    Author: shaoziyang
    Date:   2018.3

    http://www.micropython.org.cn

'''
from machine import Pin
import time
import TM1637

dio = Pin(5, Pin.OUT)
clk = Pin(4, Pin.OUT)
tm=TM1637.TM1637(dio=dio,clk=clk)

n = 0
while 1:
    tm.shownum(n)
    n += 1
    time.sleep_ms(1000)
