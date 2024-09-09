# LCD1602 Big Digits

Display large font numbers on LCD1602, ported from the [small display BIG DIGITS project](https://github.com/upiir/character_display_big_digits), please visit the project link to view the font image.

**usage**

```
from lcd1602_bigdigit import LCD1602_BIGDIGIT
from machine import I2C, Pin
from time import sleep_ms

i2c = I2C(1, sda = Pin(18), scl = Pin(16))

lcd = LCD1602_BIGDIGIT(i2c, 39)
lcd.font('square_three')

n = 0
while 1:
    n+=1
    lcd.number(n)
    sleep_ms(1000)

```

![](https://user-images.githubusercontent.com/117754156/230296829-0aea22ec-64da-4251-bfc0-5bbacfc92c3e.jpg)


From microbit/micropython Chinese community.  
www.micropython.org.cn
