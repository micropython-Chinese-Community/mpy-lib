'''

  make big digit font from "small_16x2_display_big_digits__upir.ino".
  
'''

print('Make fonts from "small_16x2_display_big_digits__upir.ino"')

f = open('small_16x2_display_big_digits__upir.ino', 'rt')
buf = f.readlines()
f.close()

linecnt = len(buf)

fontname = ''

BIGFONT = {}

def mt(n):
    return (int(n)+2)%256

for i in range(linecnt):
    p = buf[i].find('_00[8] PROGMEM')
    if p>10:
        fontname = buf[i][11:p]
        fontdat = bytearray(64)
        fontdig = bytearray(20)
        for n in range(8):
            x = p
            for m in range(8):
                x = buf[i+n].find('B' ,x+6)
                s = '0'+buf[i+n][x:x+6]
                fontdat[n*8+m]=int(s, 2)
                
    p = buf[i].find('_digits[10][4] = ')
    if p>4:
        if buf[i][5:p] == fontname:
            s = buf[i][p+len('_digits[10][4] = '):]
            s = s.replace('{','').replace('}','').replace(';','')
            d=s.split(',')
            for n in range(20):
                fontdig[n] = mt(d[n*2])*16+mt(d[n*2+1])
            BIGFONT[fontname] = [fontdat, fontdig]            

        fontname = ''

print('FONT number:', len(BIGFONT))
print('BIGFONTS = {')
x = list(BIGFONT.keys())
for i in range(len(x)):
    print("    '{}':[{},{}],".format(x[i],bytes(BIGFONT[x[i]][0]),bytes(BIGFONT[x[i]][1])))
print('}')

