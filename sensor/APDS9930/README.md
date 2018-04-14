# APDS9930 Digital Proximity and Ambient Light Sensor drive for microbit

![](apds9930.jpg)

## I2C Address

**0x39**

## API

* **AGAIN(gain=None)**  
get/set ALS Gain.
gain is: [1, 8, 16, 120] 

* **PGAIN(gain=None)**  
get/set Proximity Gain.
gain is: [1, 2, 4, 8] 

* **Power(on=True)**  
set power on/off

* **poweron()**  
goto normal mode

* **ALS_Enable(on=True)**  
Enable/Disable ALS feature

* **Wait_Enable(on=True)**  
Enable/Disable Wait Timer feature

* **Proximity_Enable(on=True)**  
Enable/Disable Proximity feature  
**VL** pin must connect to 3.3V before enable Proximity feature.

* **getALS()**  
get Ambient Light (lux)

* **getProximity()**  
get Proximity value.  
**VL** pin must connect to 3.3V before enable Proximity feature.



## example

```
from machine import Pin, I2C
import time
import APDS9930

i2c=I2C(sda=Pin(5),scl=Pin(4))

apds = APDS9930.APDS9930(i2c)

while True:
    time.sleep_ms(500)
    apds.getALS()

```

From microbit/micropython Chinese community.  
www.micropython.org.cn
