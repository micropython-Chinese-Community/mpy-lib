# [mpy-lib](https://github.com/micropython-Chinese-Community/mpy-lib)

## AHT20 SENSOR 


## Example


```py
from machine import I2C, Pin
from aht20 import AHT20
from time import sleep_ms

i2c = I2C(0, sda = Pin(4), scl = Pin(5))
aht = AHT20(i2c)

while 1:
    aht.measure()
    print('Humi: {:.2f} %, Temp: {:.2f} C'.format(aht.Humi(), aht.Temp()))
    sleep_ms(1000)
```
