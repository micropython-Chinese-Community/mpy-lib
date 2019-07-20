# LSM6DSO sensor

https://www.st.com/zh/mems-and-sensors/lsm6dso.html

## example

```
from machine import I2C
import LSM6DSO

i2c = I2C(1)
lsm = LSM6DSO.LSM6DSO(i2c)
lsm.ax()
lsm.get_a()
lsm.get()
```

From microbit/micropython Chinese community.  
www.micropython.org.cn
