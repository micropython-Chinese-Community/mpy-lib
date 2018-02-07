# BMP180 Digital pressure sensor

## I2C Address

**0x77**

## API

* **get()**  
get envirment temperature and pressure  

* **getTemp()**  
get envirment temperature 

* **getPress()**  
get Pressure

* **getAltitude()**  
Calculating absolute altitude


## example


```
from machine import I2C
import time

import bmp180

b = bmp180.BMP180(I2C(1))

while True:
    time.sleep_ms(500)
    b.get()

```

From microbit/micropython Chinese community.  
www.micropython.org.cn
