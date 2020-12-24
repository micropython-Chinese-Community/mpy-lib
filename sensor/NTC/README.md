# NTC thermistor 

NTC thermistor Sensor

![](ntc.jpg)



## example

```python
from machine import ADC, Pin

ADC_TEMP = ADC(Pin(34))
T = NTC(ADC_TEMP.read())
```

From microbit/micropython Chinese community.  
www.micropython.org.cn