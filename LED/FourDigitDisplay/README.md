# Four Digit Display TM1650/HBS650 drive

Four Digit Display is a Module with four 7-segment LED, it can show number. It has TM1650 chip inside, control with a I2C bus. 

![](4-LED.jpg)

## I2C Address

| command  | Display     |
| ---      | ---         |
| 0x24     | 0x34 - 0x37 |


## API

* **intensity(dat = -1)**  
set display intensity.  
**dat** is intensity will be set, it can be [0 - 8]. if dat is zero, display will be turn off.  
if not dat given, or dat > 8, or dat < 0, it will return current intensity.

* **on()**  
turn on display  

* **off()**  
turn off display  

* **clear（）**  
clear content of the display  

* **shownum(num)**  
show a interger number in display.  

* **showhex(num)**  
show a hex number.  

* **showDP(bit = 1, show = True)**  
show or hide dot piont in give bit  
bit is dot piont position, [0 - 3]  
show, True will show DP, other will hide it  

## example


```
import machine
import time
import FourDigitDisplay

i2c = machine.I2C(1)
fdd = FourDigitDisplay.FourDigitDisplay(i2c)

n = 0
while 1:
    fdd.shownum(n)
    n += 1
    time.sleep_ms(1000)
```

From microbit/micropython Chinese community.  
www.micropython.org.cn
