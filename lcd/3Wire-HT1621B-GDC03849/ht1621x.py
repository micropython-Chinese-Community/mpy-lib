# -*- coding:UTF-8 -*-

'''
MIT License

Copyright (c) 2018 Robin Chen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

'''
/******************************************************************************
* File       : ht1621x.py
* Function   : Drive ht1621x.
* Description: To be done.
* Version    : V0.13
* Author     : Robin Chen
* Date       : 9th May 2018
* History    :  No.  When           Who           What
*               1    9/May/2018     Robin Chen    Create
*               1    11/May/2018    Robin Chen    command to bin
*               1    17/May/2018    Robin Chen    Create
*               1    30/May/2018    Robin Chen    Code encapsulation
******************************************************************************/'''

from micropython import const
from time import sleep_ms, sleep_us, sleep

# Command list
# -------------------------
# Function Flag(Flag)
FLAG_CMD      = const(0x04)  # Command
FLAG_READ     = const(0x06)  # Read
FLAG_WRITE    = const(0x05)  # Write
FLAG_MODIFY   = const(0x05)  # READ-MODIFY-WRITE

# LCD Control
CMD_LCDON     = const(0x006)  # Turn on LCD bias generator
CMD_LCDOFF    = const(0x004)  # Turn off LCD bias generator

# System Control
CMD_SYSEN     = const(0x002)  # Turn on system oscillator
CMD_SYSDIS    = const(0x000)  # Turn off both system oscillator and LCDbias generator）

# LCD 1/2 bias option
CMD_B2C2      = const(0x040)  # 2COM,1/2 bias
CMD_B2C3      = const(0x048)  # 3COM,1/2 bias
CMD_B2C4      = const(0x050)  # 4COM,1/2 bias

# LCD 1/3 bias option
CMD_B3C2      = const(0x042)  # 2COM,1/3 bias
CMD_B3C3      = const(0x04A)  # 3COM,1/3 bias
CMD_B3C4      = const(0x052)  # 4COM,1/3 bias

# System clock Set
CMD_RC256K    = const(0x030)  # System clock source, on-chip RC oscillator
CMD_EXT256K   = const(0x038)  # System clock source, external clock source
CMD_XTAL32K   = const(0x028)  # System clock source, crystal oscillator

# Time base
CMD_TIMER_EN  = const(0x00C)  # Enable time base output
CMD_TIMER_DIS = const(0x008)  # Disable time base output
CMD_CLR_TIMER = const(0x018)  # Clear the contents of time base generator

# WDT set
CMD_WDT_DIS = const(0x00A)  # Disable WDT time-out flag output
CMD_WDT_EN  = const(0x00E)  # Enable WDT time-out flag output
CMD_CLR_WDT = const(0x01C)  # Clear the contents of WDT stage

# Sound output set
CMD_TONE2K  = const(0x0C0)  # Tone frequency, 2kHz
CMD_TONE4K  = const(0x080)  # Tone frequency, 4kHz
CMD_TONEON  = const(0x012)  # Turn on tone outputs
CMD_TONEOFF = const(0x010)  # Turn off tone outputs

# Time base/WDT clock output set
CMD_F1      = const(0x140)  # Time base/WDT clock output:1Hz | The WDT time-out flag after: 4s
CMD_F2      = const(0x142)  # Time base/WDT clock output:2Hz | The WDT time-out flag after: 2s
CMD_F4      = const(0x144)  # Time base/WDT clock output:4Hz | The WDT time-out flag after: 1s
CMD_F8      = const(0x146)  # Time base/WDT clock output:8Hz | The WDT time-out flag after: 1/2s
CMD_F16     = const(0x148)  # Time base/WDT clock output:16Hz | The WDT time-out flag after: 1/4s
CMD_F32     = const(0x14A)  # Time base/WDT clock output:32Hz | The WDT time-out flag after: 1/8s
CMD_F64     = const(0x14C)  # Time base/WDT clock output:64Hz | The WDT time-out flag after: 1/16s
CMD_F128    = const(0x14E)  # Time base/WDT clock output:128Hz | The WDT time-out flag after: 1/32s

# IRQ set
CMD_IRQ_DIS = const(0x100)  # Disable IRQ output
CMD_IRQ_EN  = const(0x110)  # Enable IRQ output

# Work mode set
CMD_TEST    = const(0x1C0)  # Test mode, user don't use
CMD_NORMAL  = const(0x1C6)  # Normal mode

# -------------- End -----------------

class HT1621B:
    '''/******************************************************************************
    * Name       : __init__(self, _cs, _rd, _wr, _htdata)
    * Function   : IC pin initialization.
    * Input      : _cs:CS Pin
    *              _rd:RD Pin
    *              _wr:WR Pin
    *              _htdata:DATA Pin
    * Output:    : None.
    * Return     : None.
    * Description: To be done.
    * Version    : V1.00
    * Author     : Robin Chen
    * Date       : 30th May 2018
    ******************************************************************************/'''
    def __init__(self, _cs, _rd, _wr, _htdata):
        self.CS = _cs      # Define the CS Pin
        self.RD = _rd      # Define the RD Pin
        self.WR = _wr      # Define the WR Pin
        self.DA = _htdata  # Define the DATA Pin
        self.CS.init(self.CS.OUT, self.CS.PULL_UP, value=1)
        self.RD.init(self.RD.OUT, self.RD.PULL_UP, value=1)
        self.WR.init(self.WR.OUT, self.WR.PULL_UP, value=1)
        self.DA.init(self.DA.OUT, self.DA.PULL_UP, value=1)
        self.init()


    '''/******************************************************************************
    * Name       : init(self,_timer = CMD_TIMER_DIS,_wdt = CMD_WDT_DIS,_scs = CMD_RC256K,
    *              _bias = CMD_B3C4,_tone = CMD_TONE4K,_irq = CMD_IRQ_DIS, _twc = CMD_F128, 
    *    		   _mod = CMD_NORMAL)
    * Function   : HT1621B parameter initialization.
    * Input      :_timer: Disable time base set
    *             _wdt  : Disable WDT set
    *             _scs  : System clock source, on-chip RC oscillator 
    *             _bias : LCD bias option and commons option set
    *             _tone : Tone Set
    *             _irq  : IRQ Set
    *             _twc  : Time base/WDT clock set
    *             _mod  : Work mode Set
    * Output:    : None.
    * Return     : None.
    * Description: To be done.
    * Version    : V1.00
    * Author     : Robin Chen
    * Date       : 30th May 2018
    ******************************************************************************/'''
    def init(self,
             _timer = CMD_TIMER_DIS,
             _wdt   = CMD_WDT_DIS,
             _scs   = CMD_RC256K,
             _bias  = CMD_B3C4,
             _tone  = CMD_TONE4K,
             _irq   = CMD_IRQ_DIS,
             _twc   = CMD_F128,
             _mod   = CMD_NORMAL
             ):

        # commend list
        lcmd = (_timer, _scs, _bias, _irq, _twc, _mod, CMD_CLR_TIMER, CMD_CLR_WDT)

        self.CS.on()
        self.WR.on()
        self.RD.on()
        self.DA.on()
        sleep(1)
        self.HT1621xWrCmd(CMD_SYSDIS)
        self.HT1621xWrCmd(_wdt)
        self.HT1621xWrCmd(CMD_SYSEN)

        for cmd in lcmd:
            self.HT1621xWrCmd(cmd)
        self.ALLCLEAR(0, 32)

        return True

    '''/******************************************************************************
    * Name       : _wrData(self, _da)
    * Function   : Write 1 data to ht1621b 
    * Input      : _da: 9 bit data
    * Output:    : None.
    * Return     : None.
    * Description: To be done.
    * Version    : V1.00
    * Author     : Robin Chen
    * Date       : 30th May 2018
    ******************************************************************************/'''
    def _wrData(self, _da):
        for i in _da:
            self.WR.off()
            self.DA.value(int(i))
            sleep_us(4)
            self.WR.on()
            sleep_us(4)
        return True


    '''/******************************************************************************
    * Name       : HT1621xWrCmd(self, _cmd)
    * Function   : send 1 commend to ht1621
    * Input      : _cmd: commend code
    * Output:    : None.
    * Return     : None.
    * Description: To be done.
    * Version    : V1.00
    * Author     : Robin Chen
    * Date       : 30th May 2018
    ******************************************************************************/'''
    def HT1621xWrCmd(self, _cmd):
        FC = bin(FLAG_CMD)[2:]
        CMD = bin(_cmd ^ (1 << 9))[3:]
        self.CS.off()
        sleep_us(4)
        self._wrData(FC)
        self._wrData(CMD)
        self.CS.on()
        sleep_us(4)
        return True


    '''/******************************************************************************
    * Name       : HT1621xWrOneData(self, _addr, _htdata)
    * Function   : Successive Address Writing One Data
    * Input      : _addr: 6 bit Address
    *              _htdata: 4 bit Data,is a list
    * Output:    : None.
    * Return     : None.
    * Description: To be done.
    * Version    : V1.00
    * Author     : Robin Chen
    * Date       : 30th May 2018
    ******************************************************************************/'''
    def HT1621xWrOneData(self, _addr, _htdata):
        FW = bin(FLAG_WRITE)[2:]
        ad = bin(_addr ^ (1 << 6))[3:]    # hex to 6 bit bin
        da = bin(_htdata ^ (1 << 4))[3:]  # hex to 4 bit bin
        self.CS.off()
        sleep_us(4)
        self._wrData(FW)
        self._wrData(ad)
        self._wrData(da)
        self.CS.on()
        sleep_us(4)
        return True


    '''/******************************************************************************
    * Name       : HT1621xWrAllData(self, _addr, _htdata)
    * Function   : Successive Address Writing Multiple Consecutive Data
    * Input      : _addr: 6 bit Address
    *              _htdata: 4 bit * 32 Data,
    * Output:    : None.
    * Return     : None.
    * Description: To be done.
    * Version    : V1.00
    * Author     : Robin Chen
    * Date       : 30th May 2018
    ******************************************************************************/'''
    def HT1621xWrAllData(self, _addr, _htdata):
        FW = bin(FLAG_WRITE)[2:]
        ad = bin(_addr ^ (1 << 6))[3:]
        self.CS.off()
        sleep_us(4)
        self._wrData(FW)         # write commend
        self._wrData(ad)         # write address
        for da in _htdata:
            dat = bin(da ^ (1 << 4))[3:]
            self._wrData(dat)    # write data
        self.CS.on()
        sleep_us(4)
        return True


    '''/******************************************************************************
    * Name       : ALLSHOW(self, _addr, _nbit)
    * Function   : All Memory is set 1
    * Input      : _addr: 6 bit Start Address
    *              _nbit: 1~32
    * Output:    : None.
    * Return     : None.
    * Description: To be done.
    * Version    : V1.00
    * Author     : Robin Chen
    * Date       : 30th May 2018
    ******************************************************************************/'''
    def ALLSHOW(self, _addr, _nbit):
        htdata = []
        for i in range(_nbit):
            htdata.append(0x0F)
        self.HT1621xWrAllData(_addr, htdata)
        return True


    '''/******************************************************************************
    * Name       : ALLCLEAR(self, _addr, _nbit)
    * Function   : All Memory is set 0
    * Input      : _addr: 6 bit Start Address
    *              _nbit: 1~32
    * Output:    : None.
    * Return     : None.
    * Description: To be done.
    * Version    : V1.00
    * Author     : Robin Chen
    * Date       : 30th May 2018
    ******************************************************************************/'''
    def ALLCLEAR(self, _addr, _nbit):
        htdata = []
        for i in range(_nbit):
            htdata.append(0x00)
        self.HT1621xWrAllData(_addr, htdata)
        return True


    '''/******************************************************************************
    * Name       : LCDON(self)
    * Function   : LCD ON
    * Input      : None.
    * Output:    : None.
    * Return     : None.
    * Description: To be done.
    * Version    : V1.00
    * Author     : Robin Chen
    * Date       : 30th May 2018
    ******************************************************************************/'''
    def LCDON(self):
        self.HT1621xWrCmd(CMD_LCDON)
        return True


    '''/******************************************************************************
    * Name       : LCDOFF(self)
    * Function   : LCD OFF
    * Input      : None.
    * Output:    : None.
    * Return     : None.
    * Description: To be done.
    * Version    : V1.00
    * Author     : Robin Chen
    * Date       : 30th May 2018
    ******************************************************************************/'''
    def LCDOFF(self):
        self.HT1621xWrCmd(CMD_LCDOFF)
        return True


    '''/******************************************************************************
    * Name       : HTBEEP(self, _t)
    * Function   : BEEP Control
    * Input      : _t: BEEP Continuous ringing time
    * Output:    : None.
    * Return     : None.
    * Description: To be done.
    * Version    : V1.00
    * Author     : Robin Chen
    * Date       : 30th May 2018
    ******************************************************************************/'''
    def HTBEEP(self, _t):
        self.HT1621xWrCmd(CMD_TONEON)
        sleep(_t)
        self.HT1621xWrCmd(CMD_TONEOFF)
        return True
