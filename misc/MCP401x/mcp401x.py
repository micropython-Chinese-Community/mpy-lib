from micropython import const

class MCP401x:

    def __init__(self, i2c, addr = 47):
        self.i2c = i2c
        self.addr = addr
        self.tb = bytearray(1)
        self.rb = bytearray(1)

    def write(self, dat):
        self.tb[0] = dat
        self.i2c.writeto(self.addr, self.tb)
        
    def read(self):
        self.i2c.readfrom_into(self.addr, self.rb)
        return self.rb[0]