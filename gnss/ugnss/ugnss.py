'''
    mini GNSS Data analysis

'''

class uGNSS():

    GNSS_DIR = ('N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S',
                'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW')
    GNSS_VALID = (b'1', b'2')

    def __init__(self, bufsize = 2048):

        self.latitude = 0.0
        self.longitude = 0.0
        self.latitude_dir = 'N'
        self.longitude_dir = 'E'
        self.speed = 0.0
        self.course = 0.0
        self.altitude = 0.0
        self.geoid_height = 0.0
        self.date = [0, 0, 0]
        self.time = [0, 0, 0]
        self.datetime = [0, 0, 0, 0, 0, 0, 0, 0]
        self.valid = False
        self.satellites_in_view = 0
        self.satellites_in_use = 0
        self.satellites_used = []
        self.hdop = 0.0
        self.pdop = 0.0
        self.vdop = 0.0
        self._crc = bytearray(1)
        self._buf = bytearray(256)
        self._pos = 0
        self._seg = []

    def DM2DMS(dm):
        return

    def checksum(self, buf, length):
        self._crc[0] = 0
        for i in range(1, length):
            self._crc[0] ^= buf[i]
        try:
            d = int(b'0x'+buf[length+1:length+3])
        except:
            return False
        return self._crc[0] == d

    def parse(self):
        try:
            if not self.checksum(self._buf, self._pos-4):
                return False

            self._seg = bytes(self._buf[1:self._pos-4]).split(b',')
            if self._seg[0] in self.GNSS_CMD:
                try:
                    self.GNSS_CMD[self._seg[0]](self)
                    return True
                except:
                    return False

            return False
        finally:
            self._pos = 0

    def update_char(self, c):
        if self._pos:
            if self._pos > 250:
                self._pos = 0
                return False
            else:
                if type(c) is int:
                    self._buf[self._pos] = c
                elif type(c) is str:
                    self._buf[self._pos] = ord(c)
                else:
                    self._pos = 0
                    return False

                if self._buf[self._pos] == ord('\n'):
                    return self.parse()
                else:
                    self._pos += 1
        else:
            if c == '$' or c == ord(b'$'):
                self._buf[0] = 36
                self._pos = 1

    def update(self, dat):
        if not dat:
            return False

        for i in range(len(dat)):
            self.update_char(dat[i])
        return self.valid

    def _time(self, dat):
        h, m, s = dat[0:2], dat[2:4], dat[4:6]
        self.time = [int(h), int(m), int(s)]
        self.datetime[4:7] = self.time
    
    def _date(self, dat):
        d, m, y = dat[0:2], dat[2:4], dat[4:6]
        self.date = [int(y), int(m), int(d)]
        self.datetime[0:3] = self.date
        
    def _latlon(self, dat):
        t = float(dat)
        d, m = divmod(t, 100)
        return d + m/60

    def _GNGGA(self):
        self._time(self._seg[1])
        self.latitude = self._latlon(self._seg[2])
        self.latitude_dir = self._seg[3].decode()
        self.longitude = self._latlon(self._seg[4])
        self.longitude_dir = self._seg[5].decode()
        self.valid = self._seg[6] in self.GNSS_VALID
        self.satellites_in_use = int(self._seg[7])
        self.hdop = float(self._seg[8])
        self.altitude = float(self._seg[9])
        self.geoid_height = float(self._seg[11])

    def _GNRMC(self):
        self._time(self._seg[1])
        self._date(self._seg[9])
        self.valid = (self._seg[2] == b'A')
        self.latitude = self._latlon(self._seg[3])
        self.latitude_dir = self._seg[4].decode()
        self.longitude = self._latlon(self._seg[5])
        self.longitude_dir = self._seg[6].decode()
        self.speed = float(self._seg[7])
        self.course = float(self._seg[8])

    def _GNVTG(self):
        self.course = float(self._seg[1])
        self.speed = float(self._seg[7])

    def _GNGLL(self):
        self.latitude = self._latlon(self._seg[1])
        self.latitude_dir = self._seg[2]
        self.longitude = self._latlon(self._seg[3])
        self.longitude_dir = self._seg[4]
        self._time(self._seg[5])
        self.valid = (self._seg[6] == b'A')
    
    def _GNGSA(self):
        self.pdop = float(self._seg[15])
        self.hdop = float(self._seg[16])
        self.vdop = float(self._seg[17])

    def _GPGSV(self):
        self.satellites_in_view = int(self._seg[3])

    GNSS_CMD = {
        b'GNGGA': _GNGGA,
        b'GNRMC': _GNRMC,
        b'GNVTG': _GNVTG,
        b'GNGLL': _GNGLL,
        b'GPGSV': _GPGSV,
        b'GNGSA': _GNGSA
    }
    
    def print(self):
        print('GNSS valid:', self.valid)
        print('lat:', self.latitude, self.latitude_dir)
        print('lon:', self.longitude, self.longitude_dir)
        print('speed:', self.speed)
        print('altitude:', self.altitude, self.geoid_height)
        print('hdop:', self.hdop)
        print('pdop:', self.pdop)
        print('vdop:', self.vdop)
        print('UTC:', self.datetime, self.date, self.time)
        print('satellites')
        print('  in view:', self.satellites_in_view)
        print('  in use: ', self.satellites_in_use)
        print('  list:   ', self.satellites_used)

