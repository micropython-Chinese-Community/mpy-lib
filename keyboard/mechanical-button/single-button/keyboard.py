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
******************************************************************************
* 文  件：keyboard.py
* 概  述：识别单个机械按键的单击、连击（暂未限制连击次数）、长按、短按动作，并返回事件。
* 版  本：V0.10
* 作  者：Robin Chen
* 日  期：2018年7月26日
* 历  史： 日期             编辑           版本         记录
          2018年7月26日    Robin Chen      V0.10       创建文件
`
******************************************************************************'''
class KEYBOARD:
    cont = 0
    def __init__(self, _btnKey, _tmBtn, _btnDef = 1, even_djlong = None, even_lj = None, _pull = None):
        self.btn = _btnKey
        if _pull == "UP":
            self.btn.init(_btnKey.IN, _btnKey.PULL_UP)
        elif _pull == "DOWN":
            self.btn.init(_btnKey.IN, _btnKey.PULL_DOWN)
        else:
            self.btn.init(_btnKey.IN)
        self.btnDef = _btnDef
        self.eve_btnLon = even_djlong
        self.evn_Continuous_Clicks = even_lj
        self.btnLabDown = 0                     # 按钮扫描记次,按下状态
        self.btnLabUp = 0                       # 按钮扫描记次,弹起状态
        self.Continuous_Clicks = 0              # 连续点击次数
        self.clock = 10                         # 定时器时钟，单位毫秒
        _tmBtn.init(freq = (1000 / self.clock))
        _tmBtn.callback(self.doBtnScan)
        self.staLon = 1                         # 长按标志字，1：长按计时，0:长按计次
        self.tLon = 3000                        # 计时或计次延时，单位毫秒
        self.TIME_CONT_CLICKS = 50              # 连击时间间隔，按下和松开的状态保持时间长度，单位，次

    '''*************************************************************************
    * 功   能：按键扫描
    * 说   明：定时器回调函数，用于识别当前按键是否动作，并判断其动作形式。
    * 输入参数：
              t : 定时器无参回调函数必备，否则调用不成功。
    * 输出参数：None
    * 返 回 值：True
    **************************************************************************'''
    # 扫描按键，定时中断调用函数
    def doBtnScan(self, t):
        global cont
        self.btnLabUp = (self.btnLabUp * int(not(self.btn.value() ^ int(not(self.btnDef))))) + int(not(self.btn.value() ^ int(not(self.btnDef))))
        btdown = self.btnLabDown
        self.btnLabDown = (self.btnLabDown * int(not(self.btn.value() ^ self.btnDef))) + int(not(self.btn.value() ^ self.btnDef))

        # 长按计时/计次
        # t1:按键保持按下的时长
        if (self.btnLabDown * self.clock) == self.tLon:
            if self.staLon == 1:
                if self.eve_btnLon != None:
                    self.eve_btnLon()               # 按键长按事件，请勿在事件中执行过长时间的程序，否则会报定时器错误。
            elif self.staLon == 0:
                if self.eve_btnLon != None:
                    cont += 1
                    self.eve_btnLon(cont)           # 按键长按事件，请勿在事件中执行过长时间的程序，否则会报定时器错误。
                self.btnLabDown = 0
        if self.btnLabUp > 5:
            cont = 0

        # 连续点击
        if (btdown > 5 and btdown < self.TIME_CONT_CLICKS) and self.btnLabUp > 0:
            self.Continuous_Clicks += 1

        if (self.btnLabUp > self.TIME_CONT_CLICKS) and (self.Continuous_Clicks > 0) or (self.btnLabDown > self.TIME_CONT_CLICKS) and (self.Continuous_Clicks > 0):
            if self.evn_Continuous_Clicks != None:
                self.evn_Continuous_Clicks(self.Continuous_Clicks)    # 连续点击事件，次数为1时为单击，请勿在事件中执行过长时间的程序，否则会报定时器错误。
            self.Continuous_Clicks = 0
