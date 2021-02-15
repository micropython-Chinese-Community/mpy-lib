**LSM303AH**, ST's ultra-low-power 3D accelerometer and 3D magnetometer.


## example

Normal mode

```python
from lsm303ah import LSM303AH
from machine import Pin, I2C

i2c = I2C(1, freq=400000)
mag = LSM303AH(i2c)
mag.m()
mag.a()
```



IRQ mode

```python
from lsm303ah import LSM303AH
from machine import Pin, I2C

i2c = I2C(1, freq=400000)
mag = LSM303AH(i2c)

def MAG_IRQ(t):
    pyb.LED(1).toggle()
    print('M:', mag.m())

mag.mag_irq(1, Pin('PA5'), MAG_IRQ)

```

