# STTS751 temperature seneor

* https://www.st.com/content/st_com/zh/products/mems-and-sensors/temperature-sensors/stts751.html


## example

```
from machine import I2C
import STTS751

i2c = I2C(1)
stt = STTS751.STTS751(i2c)
stt.temperature()
```

From microbit/micropython Chinese community.  
www.micropython.org.cn
