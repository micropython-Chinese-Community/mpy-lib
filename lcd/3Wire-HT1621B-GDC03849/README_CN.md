English

3Wire-HT1621B-GDC03849
====
![Frame diagram](./images/ht1621b_gdc.png)



HT1621B
----
HT1621B 一款LCD驱动芯片。其具有4个COM口和32个SEGO端。

参数：

name | Op
---- | ----
Val  | 20



**API**
    init(_timer = CMD_TIMER_DIS,      # 时期输出设置</BR>
         _wdt   = CMD_WDT_DIS,        # WDT溢出标志输出设置</BR>
         _scs   = CMD_RC256K,         # 系统时钟源设置</BR>
         _bias  = CMD_B3C4,           # 偏压和公共端设置</BR>
         _tone  = CMD_TONE4K,         # 声音设置</BR>
         _irq   = CMD_IRQ_DIS,        # IRQ设置（生效/失效）</BR>
         _twc   = CMD_F128,           # 时期/WDT时钟输出设置（F1～F128）</BR>
         _mod   = CMD_NORMAL          # 模式设置（测试模式和普通模式）</BR>
         ):


    def HT1621xWrCmd(self, _cmd):



GDC03849
----
GDC03849 is a LCD



API

USER
