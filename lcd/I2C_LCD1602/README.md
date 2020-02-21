# I2C LCD1602 MicroPython drive

## main feathur
- display text in I2C LCD1602
- LCD display on/off
- LCD backlight on/off
- LCD display shfit left/right

## ChangeLog

2020.2 ver 2.0
- add autoaddress() function
- add print() function
- show object in puts() function

2018.2 ver 1.0
- Initial version


![](demo.gif)


## internal signal

|LCD1602  | PCF8574A |
|--|--|
|RS  |P0  |
|RW  |P1  |
|E  |P2  |
|BackLight  |P3  |
|Dat  |P4-P7  |

## I2C Address

| PCF8574 | PCF8574A |
|--|--|
| 0x27 | 0x3F |


## API

* **on()**  
turn on LCD  

* **off()**  
turn off LCD

* **clear()**  
clear display

* **backlight(on)**  
0 turn of backlight  
1 turn on backlight

* **char(ch, x, y)**  
I2show a character in given position  
x, 0-15  
y, 0-1

* **puts(s, x, y)**  
show string/object in given position  
x, 0-15  
y, 0-1

* **print(s)**
print to LCD, auto wrap and scroll in line end.

## example

copy mp_i2c_lcd1602.py to pyboard first.

```
from machine import I2C, Pin
from mp_i2c_lcd1602 import LCD1602
from time import sleep_ms

i2c = I2C(1, sda=Pin(9), scl=Pin(10))

LCD = LCD1602(i2c)

LCD.puts("I2C LCD1602")
```

From microbit/micropython Chinese community.  
www.micropython.org.cn
