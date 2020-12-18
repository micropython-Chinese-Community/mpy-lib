# DS1307

DS1307 real-time  clock  (RTC)  is  a  low power, full binary-coded decimal (BCD) clock/calendar plus  56  bytes  of  NV  SRAM.

![](ds1307.jpg)

## I2C Address

0x68

## API

* **start()**  
start RTC.  

* **stop()**  
stop/pause RTC

* **datetime(DT = None)**  
get / set DateTime. If no paramter given, it will return current datetime, otherwise it will set datatime.  
datatime format: [year, month, day, weekday, hour, minute, second]

* **year(year = None)**  
get / set year.  

* **month(month = None)**  
get / set month.  

* **day(day = None)**  
get / set day.  

* **weekday(weekday = None)**  
get / set month.  

* **hour(hour = None)**  
get / set hour.  

* **minute(minute = None)**  
get / set minute.  

* **second(second = None)**  
get / set second.  

* **ram(reg, dat = None)**  
get / set ram data (56 bytes).  


## example

```
import ds1307
from machine import I2C, Pin

i2c = I2C(sda = Pin(5), scl=Pin(4))
ds = ds1307.DS1307(i2c)

ds.datetime()
ds.datetime([2018, 3, 9, 4, 23, 0, 1, 0])

ds.hour()
```

From microbit/micropython Chinese community.  
www.micropython.org.cn
