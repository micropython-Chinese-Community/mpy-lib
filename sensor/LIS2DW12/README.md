# LIS2DW12 motion sensor

https://www.st.com/en/mems-and-sensors/lis2dw12.html

## example

```
from machine import I2C
import LIS2DW12

i2c = I2C(1)
lis = LIS2DW12.LIS2DW12(i2c)
lis.x()
lis.get()
```

From microbit/micropython Chinese community.  
www.micropython.org.cn
