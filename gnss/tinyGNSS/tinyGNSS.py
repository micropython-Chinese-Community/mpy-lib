'''
    tiny GNSS drive

    Author: shaoziyang
    Date:   2026.7

    https://github.com/shaoziyang
'''
class tinyGNSS():

    def __init__(self, uart):
        self.uart = uart
        self.latitude, self.longitude = 0.0, 0.0
        self.latitude_dir, self.longitude_dir = 'N', 'E'
        self.speed, self.course = 0.0, 0.0
        self.year, self.month, self.day = 0, 0, 0
        self.hour, self.minute, self.second = 0, 0, 0
        self.valid = False
        self._cs = bytearray(1)
        self.buf = b''
        self.UPDATED = False

    def checksum(self, dat):
        length=len(dat)
        if dat[-1] == 10:
            length -= 2
        if dat[0] != 36 or dat[length-3] != 42:
            return False
        
        self._cs[0] = 0
        for i in range(1, length-3):
            self._cs[0] ^= dat[i]
        return self._cs[0] == int(dat[length-2:length], 16)

    def parse(self, dat, check = True):
        if len(dat) > 20 and dat[3:6] == b'RMC':
            if check:
                if not self.checksum(dat):
                    return
            
            r = dat.split(b',')
            if len(r)<9:
                return

            if r[1]:
                self.hour, self.minute, self.second = int(r[1][0:2]), int(r[1][2:4]), int(r[1][4:6])
            else:
                self.hour, self.minute, self.second = 0, 0, 0
            self.valid = (r[2] == b'A')
            self.latitude = float(r[3]) if r[3] else 0
            self.latitude_dir = r[4].decode()
            self.longitude = float(r[5]) if r[5] else 0
            self.longitude_dir = r[6].decode()
            self.speed = float(r[7]) if r[7] else 0
            self.course = float(r[8]) if r[8] else 0
            if r[9]:
                self.day, self.month, self.year = int(r[9][0:2]), int(r[9][2:4]), 2000+int(r[9][4:6])
            else:
                self.day, self.month, self.year = 0, 0, 0
            self.UPDATED = True

    def datetime(self):
        return (self.year, self.month, self.day, 0, self.hour, self.minute, self.second, 0)
        
    def update(self, showinfo=False, showdat=False):
        try:
            self.UPDATED = False
            while self.uart.any():
                self.buf = self.buf + self.uart.readline()
                if self.buf[-1] == 10:
                    if showdat:
                        print(self.buf)
                    self.parse(self.buf)
                    self.buf = b''
                if len(self.buf) > 200:
                    self.buf = b''
            if showinfo:
                self.info()
        except Exception as e:
            print(e)
    
    def info(self):
        print('GNSS updated:', self.UPDATED)
        print('GNSS valid:', self.valid)
        print('lat:', self.latitude, self.latitude_dir)
        print('lon:', self.longitude, self.longitude_dir)
        print('speed:', self.speed)
        print('course:', self.course)
        print('UTC:', self.datetime(), '\n')
