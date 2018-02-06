# I2C LCD1602


## link

| pyboard | LCD1602 |
|--|--|
| 3V | VCC |
| GND | GND |
| SCL1 | SCL |
| SDA1 | SDA |


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
show a character in given position  
x, 0-15  
y, 0-1

* **puts(s, x, y)**  
show a string in given position  
x, 0-15  
y, 0-1


## example

copy mp_i2c_lcd1602.py to pyboard first.

```
import mp_i2c_lcd1602

l=mp_i2c_lcd1602.LCD1620()
l.puts('Hello!')
```

[From microbit/micropython Chinese community](www.micropython.org.cn)
