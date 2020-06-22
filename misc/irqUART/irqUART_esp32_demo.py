'''
    irqUART demo for esp32

    Author: shaoziyang
    Date:   2020.6

    http://www.micropython.org.cn
'''
from machine import Pin, UART
from irqUART import irqUART

cnt = 0
def U1_RX_IRQ(t):
    global cnt
    n = 0
    while u1.any():
        d = u1.any()
        cnt+=d
        n+=1
        print('[', n, ']', cnt, d, u1.read(d))

def U1_RX_FRAME_IRQ(t):
    global cnt
    print('FRAME end')
    cnt = 0

# ESP32
u1=UART(2, 115200, tx=23, rx=22)
ui = irqUART(u1, Pin(22), U1_RX_IRQ, U1_RX_FRAME_IRQ)
ui.uart.init(115200)


