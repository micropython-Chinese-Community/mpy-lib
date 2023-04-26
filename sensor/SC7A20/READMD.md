# [mpy-lib](https://github.com/micropython-Chinese-Community/mpy-lib)

## SC7A20 3-AXIS ACCELEROMETER SENSOR 

<img width = '200' height ='165' src ="https://www.silan.com.cn/en/upload/2020/03/31/1585637043217ivfnz.png">

- https://www.silan.com.cn/en/index.php/product/details/47.html

The SC7A20 is an acceleration sensor IC, which features abundant functions, low power dissipation, small size, and precision measurement.

## Example


```py
from machine import I2C, Pin
from time import sleep_ms

from SC7A20 import SC7A20

i2c = I2C(0, sda=Pin(4), scl=Pin(16))

sc = SC7A20(i2c)

while True:
    print(sc.x(), sc.y(), sc.z())
    sleep_ms(100)
```
