from lcd1602_bigdigit import LCD1602_BIGDIGIT
from machine import I2C, Pin
from time import sleep_ms

#i2c = I2C(1, sda=Pin(27), scl=Pin(26))
i2c = I2C(1, sda = Pin(18), scl = Pin(16))

lcd = LCD1602_BIGDIGIT(i2c, 39)
lcd.font('square_three')

n = 0
while 1:
    n+=1
    lcd.number(n,4)
    sleep_ms(1000)
