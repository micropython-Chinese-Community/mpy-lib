# LPS22HB/HD/HH pressure seneor

* https://www.st.com/content/st_com/en/products/mems-and-sensors/pressure-sensors/lps22hb.html
* https://www.st.com/content/st_com/en/products/mems-and-sensors/pressure-sensors/lps22hd.html
* https://www.st.com/content/st_com/en/products/mems-and-sensors/pressure-sensors/lps22hh.html

![](en.LPS22HB_pressure_sensor_web.jpg)

## example

```
from machine import I2C
import LPS22

i2c = I2C(1)
lps = LPS22.LPS22(i2c)
lps.get()
```

From microbit/micropython Chinese community.  
www.micropython.org.cn
