# LIS2MDL Magnetic sensor

https://www.st.com/zh/mems-and-sensors/lis2mdl.html

## example

```
from machine import I2C
import LIS2MDL

i2c = I2C(1)
mdl = LIS2MDL.LIS2MDL(i2c)
mdl.x()
mdl.get()
```

From microbit/micropython Chinese community.  
www.micropython.org.cn
