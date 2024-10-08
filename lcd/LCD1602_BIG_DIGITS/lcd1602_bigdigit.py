'''
    mpy drive for I2C LCD1602 Big Digits

    Author: shaoziyang
    Date:   2024.9

    https://www.micropython.org.cn

'''
from i2c_lcd1602 import I2C_LCD1602

BIGFONTS = {
    'real':[b'\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1c\x02\x02\x01\x01\x02\x02\x1c\x07\x08\x08\x10\x10\x08\x08\x07\x1c\x04\x04\x04\x08\x08\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x08\x08\x07\x03\x04\x04\x08\x08\x10\x10\x1f',b'\x00T\x07\x07$S$4\x93\x07\x924\x92\x84&\x07TTT6'],
    'real_bold':[b'\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1c\x0e\x06\x07\x07\x06\x0e\x1c\x07\x0e\x0c\x1c\x1c\x0c\x0e\x07\x1e\x06\x06\x06\x0c\x0c\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x1c\x0c\x0e\x07\x03\x06\x06\x0c\x0c\x18\x18\x1f',b'\x00T\x07\x07$S$4\x93\x07\x924\x92\x84&\x07TTT6'],
    'rounded':[b'\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1c\x02\x01\x01\x01\x01\x02\x1c\x07\x08\x10\x10\x10\x10\x08\x07\x00\x00\x00\x10\x10\x10\x10\x1f\x10\x10\x10\x10\x10\x10\x10\x10\x01\x02\x04\x08\x00\x00\x00\x00\x10\x10\x10\x10\x10\x08\x04\x03',b'\x00T\x87\x07$S$4\x96\x07R4RT$\x07TTT4'],
    'rounded_bold':[b'\x1f\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x1c\x1e\x07\x03\x03\x07\x1e\x1c\x07\x0f\x1c\x18\x18\x1c\x0f\x07\x00\x00\x00\x18\x18\x18\x1f\x1f\x18\x18\x18\x18\x18\x18\x18\x18\x03\x07\x0e\x0c\x00\x00\x00\x00\x18\x18\x18\x18\x18\x0c\x07\x03',b'\x00T\x87\x07$S$4\x96\x07R4RT$\x07TTT4'],
    'skewed':[b'\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x01\x01\x01\x02\x04\x08\x10\x01\x02\x04\x08\x10\x10\x10\x1f\x1f\x10\x10\x10\x10\x10\x10\x1f\x10\x10\x10\x10\x10\x10\x10\x10\x1f\x00\x00\x00\x00\x00\x00\x1f\x1f\x10\x10\x10\x10\x10\x10\x10',b'\x00d\x07\x07$S$4S\x07\x92\x84\x92d$\x07dd\x94$'],
    'skewed_bold':[b'\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x03\x03\x03\x02\x04\x08\x10\x01\x02\x04\x08\x18\x18\x18\x1f\x1f\x18\x18\x18\x18\x18\x18\x1f\x18\x18\x18\x18\x18\x18\x18\x18\x1f\x00\x00\x00\x00\x00\x00\x1f\x1f\x18\x18\x18\x18\x18\x18\x18',b'\x00d\x07\x07$S$4S\x07\x92\x84\x92d$\x07dd\x94$'],
    'dots_small':[b'\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x15\x00\x01\x00\x00\x01\x00\x15\x15\x00\x10\x00\x00\x10\x00\x15\x15\x00\x10\x00\x00\x10\x00\x10\x10\x00\x10\x00\x00\x10\x00\x10\x15\x00\x00\x00\x00\x00\x00\x15\x10\x00\x10\x00\x00\x10\x00\x15',b'g\x97\x07\x07\x84X$4\x93\x07X\x84XT$\x07TTT\x84'],
    'dots_big':[b'\x1b\x1b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1b\x1b\x1b\x1b\x00\x03\x03\x00\x1b\x1b\x1b\x1b\x00\x18\x18\x00\x1b\x1b\x1b\x1b\x00\x18\x18\x00\x18\x18\x18\x18\x00\x18\x18\x00\x18\x18\x1b\x1b\x00\x00\x00\x00\x1b\x1b\x18\x18\x00\x18\x18\x00\x1b\x1b',b'g\x97\x07\x07\x84X$4\x93\x07X\x84XT$\x07TTT\x84'],
    'dashed':[b'\x1b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1b\x1b\x01\x00\x01\x01\x00\x01\x1b\x1b\x10\x00\x10\x10\x00\x10\x1b\x1b\x10\x00\x10\x10\x00\x10\x10\x10\x10\x00\x10\x10\x00\x10\x10\x1b\x00\x00\x00\x00\x00\x00\x1b\x10\x10\x00\x10\x10\x00\x10\x1b',b'g\x97\x07\x07\x84X$4\x93\x07X\x84XT$\x07TTT\x84'],
    'dashed_bold':[b'\x1b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1b\x1b\x03\x00\x03\x03\x00\x03\x1b\x1b\x18\x00\x18\x18\x00\x18\x1b\x1b\x18\x00\x18\x18\x00\x18\x18\x18\x18\x00\x18\x18\x00\x18\x18\x1b\x00\x00\x00\x00\x00\x00\x1b\x18\x18\x00\x18\x18\x00\x18\x1b',b'g\x97\x07\x07\x84X$4\x93\x07X\x84XT$\x07TTT\x84'],
    'angled':[b'\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x01\x01\x01\x01\x01\x01\x1f\x1f\x10\x10\x10\x10\x10\x10\x1f\x1f\x01\x01\x01\x01\x01\x01\x01\x10\x10\x10\x10\x10\x10\x10\x10\x1f\x00\x00\x00\x00\x00\x00\x1f\x01\x01\x01\x01\x01\x01\x01\x1f',b'\x00T\x07\x07&X&4S\x07R4pT$\x07TTT\t'],
    'angled_bold':[b'\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x03\x03\x03\x03\x03\x03\x1f\x1f\x18\x18\x18\x18\x18\x18\x1f\x1f\x03\x03\x03\x03\x03\x03\x03\x18\x18\x18\x18\x18\x18\x18\x18\x1f\x00\x00\x00\x00\x00\x00\x1f\x03\x03\x03\x03\x03\x03\x03\x1f',b'\x00T\x07\x07&X&4S\x07R4pT$\x07TTT\t'],
    'blocks':[b'\x1f\x1f\x1f\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x00\x00\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',b'\x11\x11\x01\x01!\x13!1\x13\x01\x121\x12\x11!\x01DU\x111'],
    'blocks_crossed':[b'\x1f\x1f\x1f\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x1f\x1f\x1e\x1d\x1b\x17\x0f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1e\x1d\x1f\x1f\x1f\x1f\x17\x0f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1e\x1d\x1b\x17\x0f\x1e\x1d\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x17\x0f',b"\x19\x81\x04\x01!C'1C\x01\x124\x12V!\x07VVV1"],
    'blocks_cut':[b'\x1f\x1f\x1f\x1f\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x1f\x1f\x01\x03\x07\x0f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x0f\x07\x03\x01\x10\x18\x1c\x1e\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1f\x1e\x1c\x18\x10\x00\x00\x00\x00\x00\x01\x03\x07\x1c\x18\x10\x00\x00\x00\x00\x00',b"A\x17\x04\x01'C!7C\x01\x127I\x17!\x07\x17AA\x87"],
    'classic':[b'\x1f\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x1f\x1f\x03\x03\x03\x03\x03\x03\x1f\x1f\x18\x18\x18\x18\x18\x18\x1f\x01\x02\x04\x00\x00\x00\x00\x00\x18\x18\x18\x18\x18\x18\x18\x18\x1f\x00\x00\x00\x00\x00\x00\x1f\x18\x18\x18\x18\x18\x18\x18\x1f',b'\x00Tg\x07\x84X$4\x93\x07X\x84XT$\x07TTT\x84'],
    'classic_bold':[b'\x1f\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x1f\x1f\x07\x07\x07\x07\x07\x07\x1f\x1f\x1c\x1c\x1c\x1c\x1c\x1c\x1f\x01\x03\x07\x00\x00\x00\x00\x00\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1f\x00\x00\x00\x00\x00\x00\x1f\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1f',b'\x00Tg\x07\x84X$4\x93\x07X\x84XT$\x07TTT\x84'],
    'classic_serif':[b'\x1f\x1f\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x1f\x1f\x1f\x03\x03\x03\x03\x03\x03\x1f\x1f\x18\x18\x18\x18\x18\x18\x1f\x1f\x00\x00\x00\x00\x00\x1f\x1f\x18\x18\x18\x18\x18\x18\x18\x18\x1f\x1f\x00\x00\x00\x00\x00\x1f\x18\x18\x18\x18\x18\x18\x18\x1f',b'\x00T\x07\x07\x84V$4\x93\x07XdXT$\x07TTTd'],
    'tron':[b'\x1f\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x1f\x1f\x03\x03\x03\x03\x03\x03\x03\x1f\x18\x18\x18\x18\x18\x18\x1f\x1f\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x1f\x00\x00\x00\x00\x00\x00\x1f\x18\x18\x18\x18\x18\x18\x18\x1f',b'd\x91\x07\x07$X$1\x93\x07X1XQ$\x07TQT\x04'],
    'tron_bold':[b'\x1f\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x1f\x1f\x07\x07\x07\x07\x07\x07\x07\x1f\x1c\x1c\x1c\x1c\x1c\x1c\x1f\x1f\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1f\x00\x00\x00\x00\x00\x00\x1f\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1f',b'd\x91\x07\x07$X$1\x93\x07X1XQ$\x07TQT\x04'],
    'square_two':[b'\x1f\x1f\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x1f\x1f\x1f\x1f\x03\x03\x03\x03\x1f\x1f\x1f\x1f\x18\x18\x18\x18\x1f\x1f\x01\x03\x07\x00\x00\x00\x00\x00\x18\x18\x18\x18\x18\x18\x18\x18\x1f\x1f\x00\x00\x00\x00\x1f\x1f\x18\x18\x18\x18\x18\x18\x1f\x1f',b'\x00Tg\x07\x84X$4\x93\x07X\x84XT$\x07TTT\x84'],
    'square_three':[b'\x1f\x1f\x1c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1c\x1f\x1f\x1f\x1f\x07\x07\x07\x07\x1f\x1f\x1f\x1f\x1c\x1c\x1c\x1c\x1f\x1f\x01\x03\x07\x0f\x00\x00\x00\x00\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1f\x1f\x00\x00\x00\x00\x1f\x1f\x1c\x1c\x1c\x1c\x1c\x1c\x1f\x1f',b'\x11Tg\x07\x84X$4\x93\x07X\x84XT$\x07TTT\x84'],
    'square_four':[b'\x1f\x1f\x1c\x1c\x00\x00\x00\x00\x00\x00\x00\x00\x1c\x1c\x1f\x1f\x1f\x1f\x0f\x0f\x0f\x0f\x1f\x1f\x1f\x1f\x1e\x1e\x1e\x1e\x1f\x1f\x01\x03\x07\x0f\x00\x00\x00\x00\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1f\x1f\x00\x00\x00\x00\x1f\x1f\x1e\x1e\x1e\x1e\x1e\x1e\x1f\x1f',b'\x11Tg\x07\x84X$4\x93\x07X\x84XT$\x07TTT\x84'],
    'square_five':[b'\x1f\x1f\x1f\x1c\x00\x00\x00\x00\x00\x00\x00\x00\x1c\x1f\x1f\x1f\x1f\x1f\x1f\x0f\x0f\x1f\x1f\x1f\x1f\x1f\x1f\x1e\x1e\x1f\x1f\x1f\x01\x03\x07\x0f\x0f\x00\x00\x00\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1e\x1f\x1f\x1f\x00\x00\x1f\x1f\x1f\x1e\x1e\x1e\x1e\x1e\x1f\x1f\x1f',b'\x11Tg\x07\x84X$4\x93\x07X\x84XT$\x07TTT\x84'],
}

class LCD1602_BIGDIGIT(I2C_LCD1602):
    
    def __init__(self, i2c, addr=0):
        self.i2c = i2c
        self.addr = addr
        super().__init__(i2c, addr)
        self.fontdat = (bytearray(64), bytearray(20))
        self.font('real')

    def font(self, fontname):
        try:
            self.fontdat = BIGFONTS[fontname]
            self.write_cgram(self.fontdat[0])
        except:
            print('Load font error!')

    # show one digit
    def digit(self, n=0, pos=0):
        n = n%10
        d1 = self.fontdat[1][n*2+0]
        d2 = self.fontdat[1][n*2+1]
        self.char((d1//16-2)%256, pos, 0)
        self.char((d1%16-2)%256)
        self.char((d2//16-2)%256, pos, 1)
        self.char((d2%16-2)%256)

    # show number
    def number(self, num=1, bits=5):
        for i in range(bits):
            self.digit(num%10, 13-i*3)
            num //= 10
