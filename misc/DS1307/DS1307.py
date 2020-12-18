'''
    DS1307 RTC drive

    Author: shaoziyang
    Date:   2018.3

    http://www.micropython.org.cn
'''
from micropython import const

DS1307_I2C_ADDRESS  = const(104)
DS1307_REG_SECOND   = const(0)
DS1307_REG_MINUTE   = const(1)
DS1307_REG_HOUR     = const(2)
DS1307_REG_WEEKDAY  = const(3)
DS1307_REG_DAY      = const(4)
DS1307_REG_MONTH    = const(5)
DS1307_REG_YEAR     = const(6)
DS1307_REG_CTRL     = const(7)
DS1307_REG_RAM      = const(8)

class DS1307():
    def __init__(self, i2c):
        self.i2c = i2c
        self.DT = [0] * 8
        self.buf = bytearray(8)
        self.tb = bytearray(1)
        self.rb = bytearray(1)
        self.start()

    # set reg
    def	setReg(self, reg, dat):
        self.tb[0] = dat
        self.i2c.writeto_mem(DS1307_I2C_ADDRESS, reg, self.tb)

    # get reg
    def	getReg(self, reg):
        self.i2c.readfrom_mem_into(DS1307_I2C_ADDRESS, reg, self.rb)
        return self.rb[0]

    def start(self):
        t = self.getReg(DS1307_REG_SECOND)
        self.setReg(DS1307_REG_SECOND, t&0x7F)

    def stop(self):
        t = self.getReg(DS1307_REG_SECOND)
        self.setReg(DS1307_REG_SECOND, t|0x80)

    def DecToHex(self, dat):
        return (dat//10) * 16 + (dat%10)

    def HexToDec(self, dat):
        return (dat//16) * 10 + (dat%16)

    def datetime(self, DT=None):
        if DT == None:
            self.i2c.readfrom_mem_into(DS1307_I2C_ADDRESS, DS1307_REG_SECOND, self.buf)
            self.DT[0] = self.HexToDec(self.buf[6]) + 2000
            self.DT[1] = self.HexToDec(self.buf[5])
            self.DT[2] = self.HexToDec(self.buf[4])
            self.DT[3] = self.HexToDec(self.buf[3])
            self.DT[4] = self.HexToDec(self.buf[2])
            self.DT[5] = self.HexToDec(self.buf[1])
            self.DT[6] = self.HexToDec(self.buf[0])
            self.DT[7] = 0
            return self.DT
        else:
            self.buf[0] = 0
            self.buf[1] = self.DecToHex(DT[6]%60)    # second
            self.buf[2] = self.DecToHex(DT[5]%60)    # minute
            self.buf[3] = self.DecToHex(DT[4]%24)    # hour
            self.buf[4] = self.DecToHex(DT[3]%8)     # week day
            self.buf[5] = self.DecToHex(DT[2]%32)    # date
            self.buf[6] = self.DecToHex(DT[1]%13)    # month
            self.buf[7] = self.DecToHex(DT[0]%100)   # year
            self.i2c.writeto(DS1307_I2C_ADDRESS, self.buf) 

    def year(self, year = None):
        if year == None:
            return self.HexToDec(self.getReg(DS1307_REG_YEAR)) + 2000
        else:
            self.setReg(DS1307_REG_YEAR, self.DecToHex(year%100))

    def month(self, month = None):
        if month == None:
            return self.HexToDec(self.getReg(DS1307_REG_MONTH))
        else:
            self.setReg(DS1307_REG_MONTH, self.DecToHex(month%13))
            
    def day(self, day = None):
        if day == None:
            return self.HexToDec(self.getReg(DS1307_REG_DAY))
        else:
            self.setReg(DS1307_REG_DAY, self.DecToHex(day%32))

    def weekday(self, weekday = None):
        if weekday == None:
            return self.HexToDec(self.getReg(DS1307_REG_WEEKDAY))
        else:
            self.setReg(DS1307_REG_WEEKDAY, self.DecToHex(weekday%8))

    def hour(self, hour = None):
        if hour == None:
            return self.HexToDec(self.getReg(DS1307_REG_HOUR))
        else:
            self.setReg(DS1307_REG_HOUR, self.DecToHex(hour%24))

    def minute(self, minute = None):
        if minute == None:
            return self.HexToDec(self.getReg(DS1307_REG_MINUTE))
        else:
            self.setReg(DS1307_REG_MINUTE, self.DecToHex(minute%60))

    def second(self, second = None):
        if second == None:
            return self.HexToDec(self.getReg(DS1307_REG_SECOND))
        else:
            self.setReg(DS1307_REG_SECOND, self.DecToHex(second%60))

    def ram(self, reg, dat = None):
        if dat == None:
            return self.getReg(DS1307_REG_RAM + (reg%56))
        else:
            self.setReg(DS1307_REG_RAM + (reg%56), dat)
