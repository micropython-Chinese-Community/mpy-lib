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

'''/******************************************************************************
* File       : gdc03849.py
* Function   : LCD Drive
* Description: To be done.
* Version    : V1.00
* Author     : Robin Chen
* Date       : 9th May 2018
* History    :  No.  When           Who           What
*               1    9/May/2018     Robin Chen    Create
*               2    30/May/2018    Robin Chen    Complete package
******************************************************************************/'''

class GDC03849:
    '''/******************************************************************************
    * Name       : __init__(self, _ht1621x)
    * Function   : Init
    * Input      : _ht1621x: object.
    * Output:    : None.
    * Return     : None.
    * Description: To be done.
    * Version    : V1.00
    * Author     : Robin Chen
    * Date       : 9th May 2018
    ******************************************************************************/'''
    def __init__(self, _ht1621x):
        self.ht = _ht1621x
        self.ht.init()      # Here you can add parameters as needed, currently using default parameters
        self.ht.LCDON()
        self.LCDALLSHOW()
        self.ht.HTBEEP(1)   # Buzzer sounds for 1 second
        self.LCDALLCLEAR()

        # the hex list for (0-9、.)
        self.NUMCODE_RH_HEX = ((0x0D, 0x0F),  # 0
                          (0x08, 0x06),
                          (0x0B, 0x0D),
                          (0x0A, 0x0F),
                          (0x0E, 0x06),
                          (0x0E, 0x0B),
                          (0x0F, 0x0B),
                          (0x08, 0x0E),
                          (0x0F, 0x0F),
                          (0x0E, 0x0F))  # 9

        # the hex list for (0-9、.)
        self.NUMCODE_TEMP_HEX = ((0x0F, 0x0D),  # 0
                            (0x06, 0x08),
                            (0x0B, 0x0E),
                            (0x0F, 0x0A),
                            (0x06, 0x0B),
                            (0x0D, 0x0B),
                            (0x0D, 0x0F),
                            (0x07, 0x08),
                            (0x0F, 0x0F),
                            (0x0F, 0x0B))  # 9

    '''/******************************************************************************
    * Name       : viewTemp(self, _gdcdata)
    * Function   : Init
    * Input      : _gdcdata: value.
    * Output:    : None.
    * Return     : None.
    * Description: To be done.
    * Version    : V1.00
    * Author     : Robin Chen
    * Date       : 9th May 2018
    ******************************************************************************/'''
    def viewTemp(self, _gdcdata):
        val = ()
        stda = ('00000' + str(int(_gdcdata * 100)))[-5::]
        stda = list(stda)[::-1]
        for i in stda:
            val = val + self.NUMCODE_TEMP_HEX[int(i)]
        self.ht.HT1621xWrAllData(0x0A, val)
        return True

    '''/******************************************************************************
    * Name       : viewRH(self, _gdcdata)
    * Function   : Value Show
    * Input      : _gdcdata: value.
    * Output:    : None.
    * Return     : None.
    * Description: To be done.
    * Version    : V1.00
    * Author     : Robin Chen
    * Date       : 9th May 2018
    ******************************************************************************/'''
    def viewRH(self, _gdcdata):
        val = ()
        stda = ('00000' + str(int(_gdcdata * 100)))[-5::]
        for i in stda:
            val = val + self.NUMCODE_RH_HEX[int(i)]
        self.ht.HT1621xWrAllData(0x00, val)
        return True

    '''/******************************************************************************
    * Name       : LCDALLSHOW(self)
    * Function   : LCD ALL Value Show
    * Input      : None.
    * Output:    : None.
    * Return     : None.
    * Description: To be done.
    * Version    : V1.00
    * Author     : Robin Chen
    * Date       : 9th May 2018
    ******************************************************************************/'''
    def LCDALLSHOW(self):
        self.ht.ALLSHOW(0x00, 20)
        return True

    '''/******************************************************************************
    * Name       : LCDALLCLEAR(self)
    * Function   : LCD ALL Clear
    * Input      : None.
    * Output:    : None.
    * Return     : None.
    * Description: To be done.
    * Version    : V1.00
    * Author     : Robin Chen
    * Date       : 9th May 2018
    ******************************************************************************/'''
    def LCDALLCLEAR(self):
        self.ht.ALLCLEAR(0x00, 20)
        return True


    '''/******************************************************************************
    * Name       : TEMPCLEAR(self)
    * Function   : Temp ALL Clear
    * Input      : None.
    * Output:    : None.
    * Return     : None.
    * Description: To be done.
    * Version    : V1.00
    * Author     : Robin Chen
    * Date       : 9th May 2018
    ******************************************************************************/'''
    def TEMPCLEAR(self):
        self.ht.ALLCLEAR(0x0A, 10)
        return True


    '''/******************************************************************************
    * Name       : RHCLEAR(self)
    * Function   : RH ALL Clear
    * Input      : None.
    * Output:    : None.
    * Return     : None.
    * Description: To be done.
    * Version    : V1.00
    * Author     : Robin Chen
    * Date       : 9th May 2018
    ******************************************************************************/'''
    def RHCLEAR(self):
        self.ht.ALLCLEAR(0x00, 10)
        return True
