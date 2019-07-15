# HTS221 sensor

https://www.st.com/content/st_com/en/products/mems-and-sensors/humidity-sensors/hts221.html

## example

```
from machine import I2C
import HTS221

i2c = I2C(1)
hts = HTS221.HTS221(i2c)
hts.get()
```

From microbit/micropython Chinese community.  
www.micropython.org.cn
