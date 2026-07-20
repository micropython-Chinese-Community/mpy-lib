# tinyGNSS

A very compact and fast GNSS driver. Only parse **RMC** messages to obtain data such as location, UTC time, speed, etc.

Usage:

```python
from machine import Pin, UART
from time import sleep

gu = UART(2, 9600, tx=Pin(42), rx=Pin(41), rxbuf=1024)
tg = tinyGNSS(gu)

while 1:
    sleep(1)
    tg.update(1)
    
```
