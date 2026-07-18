from machine import Pin, SoftSPI
from time import sleep_ms
from lcd1602_595 import LCD1602_595

#lcd = LCD1602_595(ST_CP=Pin(27), SH_CP=Pin(28), DS=Pin(26))
lcd = LCD1602_595(spi=SoftSPI(sck=Pin(28),mosi=Pin(26),miso=Pin(25)), ST_CP=Pin(27))

n = 0
while 1:
    lcd.print(f"{n}", end=' ')
    n += 1

    sleep_ms(200)
