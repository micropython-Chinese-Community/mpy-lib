# MCP401x 

7-Bit Digital POT

## example

```python
from machine import I2C, Pin
import mcp401x

i2c = I2C(sda = Pin(5), scl=Pin(4))
mcp = mcp401x.MCP401x(i2c)
mcp.write(50)

```

From microbit/micropython Chinese community.  
www.micropython.org.cn