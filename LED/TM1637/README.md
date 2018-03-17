# Four Digit Display TM1637 drive

Four Digit Display is a Module with four 7-segment LED, it can show number. It has TM1637 chip inside, control with a two line interface.  

This drive base on mcauser's TM1637 LED driver:  
https://github.com/mcauser/micropython-tm1637

![](4-LED.jpg)


## API

* **TM1637(clk, dio, intensity=7, number = 4)**  
initial TM1637 display.  
clk, clock singal.  
dio, data input/output signal.  
intensity, display intensity.  
number, LED number.  

* **intensity(val=None)**  
set display intensity.  
**val** is intensity will be set, it can be [0 - 8]. if dat is zero, display will be turn off.  
if not dat given, it will return current intensity.

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
from machine import Pin
import time
import TM1637

dio = Pin(5, Pin.OUT)
clk = Pin(4, Pin.OUT)
tm=TM1637.TM1637(dio=dio,clk=clk)

n = 0
while 1:
    tm.shownum(n)
    n += 1
    time.sleep_ms(1000)
```

From microbit/micropython Chinese community.  
www.micropython.org.cn
