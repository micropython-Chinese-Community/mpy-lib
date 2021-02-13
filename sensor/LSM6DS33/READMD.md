**LSM6DS33**, ST's always-on 3D accelerometer and 3D gyroscope sensor.



## example

Normal mode

```python
from lsm6ds33 import LSM6DS33
from machine import Pin, I2C

i2c = I2C(1, freq=400000)
gyr = LSM6DS33(i2c)
gyr.a()
gyr.g()
```



IRQ mode

```python
from lsm6ds33 import LSM6DS33
from machine import Pin, I2C

i2c = I2C(1, freq=400000)
gyr = LSM6DS33(i2c)

def GYR_IRQ(t):
    pyb.LED(1).toggle()
    print('A:', gyr.a_raw())

gyr.wakeup_mode(True, Pin('PA6'), GYR_IRQ)

```

