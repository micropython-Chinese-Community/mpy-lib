[:cn: 简体中文](./README.md)

3Wire-HT1621B-GDC03849
====
![Frame diagram](./images/ht1621b_gdc.png)
> 3Wire-HT1621B-GDC03849 为ht1621b作为驱动芯片的GDC03849液晶驱动模块。驱动芯片与主CPU为3+CS总线通讯方式进行数据交换。


HT1621B
----
> HT1621是由[台湾合泰半导体公司][]生产的一款128点内存映象和多功能的LCD驱动器，HT1621 的软件配置特性使它适用于多种LCD应用场合包括LCD模块和显示子系统用于连接主控制器和HT1621的管脚只有4或5条，HT1621 还有一个节电命令用于降低系统功耗。详细资料请阅读 [HT1621B数据手册][1]


### 接口信息

* **init(_timer = CMD_TIMER_DIS,      # 时期输出设置</BR>
         _wdt   = CMD_WDT_DIS,        # WDT溢出标志输出设置</BR>
         _scs   = CMD_RC256K,         # 系统时钟源设置</BR>
         _bias  = CMD_B3C4,           # 偏压和公共端设置</BR>
         _tone  = CMD_TONE4K,         # 声音设置</BR>
         _irq   = CMD_IRQ_DIS,        # IRQ设置（生效/失效）</BR>
         _twc   = CMD_F128,           # 时期/WDT时钟输出设置（F1～F128）</BR>
         _mod   = CMD_NORMAL          # 模式设置（测试模式和普通模式）</BR>
         )**</BR>
芯片功能与参数初始化。

* **HT1621xWrCmd(_cmd)**</BR>
*发送单个命令。*</BR>
_cmd: 命令。（16进制）</BR>
  ```python
  # 向ht1621b发送打开LCD偏置电压（即打开LCD电源）的命令
  HT1621xWrCmd(0x006)    # 在这里已经设置了常量（LCDON）来代替命令值（0x006)。

* **HT1621xWrOneData(_addr, _htdata)**</BR>
*指定地址发送单个数据。*</BR>
_addr: 地址（16进制）</BR>
_htdata:数据，通常为1个字节。（16进制）</BR>
  ```python
  # 将温度最左侧(1号位)的数字显示为2
  HT1621xWrOneData(0x13, ((0x0B, 0x06)))

* **HT1621xWrAllData(_addr, _htdata)**</BR>
*指定起始地址，连续发送多个数据。*</BR>
_addr：起始地址（16进制）</BR>
_htdata：连续的数据（16进制列表）</BR>
  ```python
  # 将温度值区全部显示为2。
  ALLSHOW(0x00, ((0x0B, 0x06), (0x0B, 0x06), (0x0B, 0x06), (0x0B, 0x06), (0x0B, 0x06), (0x0B, 0x06)))
  ```

* **ALLSHOW(_addr, _nbit)**</BR>
*指定起始地址连续发送指定个数的 1。*</BR>
_addr:起始地址（16进制）</BR>
_nbit:数据SEG位数(1-32)。</BR>
  ```python
  # 清除内存中所有内容，即全部置1
  ALLSHOW(0x00, 32)
  ```

* **ALLCLEAR(_addr, _nbit)**</BR>
*指定起始地址连续发送指定个数的 0。*</BR>
  _addr: 起始地址。（0x00-0x)</BR>
  _nbit: RAM区（SEG）个数（1-32）。</BR>
  ```python
  # 清除内存中所有内容，即全部置0
  ALLCLEAR(0x00, 32)
  ```
* **LCDON()**</BR>
*打开LCD偏压发生器。*
  
* **LCDOFF()** </BR>
*关闭LCD偏压发生器。*  

* **HTBEEP(_t)**</BR>
*使蜂鸣器一直响指定的时间后不响。*</BR>
  _t:保持时间，单位：毫秒</BR>
  ```python
  # 蜂鸣器持续响500毫秒
  HTBEEP(500)
  ```

### 常量信息


FLAG_CMD      = const(0x04)  # Command
FLAG_READ     = const(0x06)  # Read
FLAG_WRITE    = const(0x05)  # Write
FLAG_MODIFY   = const(0x05)  # READ-MODIFY-WRITE

* LCD Control
CMD_LCDON     = const(0x006)  # Turn on LCD bias generator
CMD_LCDOFF    = const(0x004)  # Turn off LCD bias generator

* System Control
CMD_SYSEN     = const(0x002)  # Turn on system oscillator
CMD_SYSDIS    = const(0x000)  # Turn off both system oscillator and LCDbias generator）

* LCD 1/2 bias option
CMD_B2C2      = const(0x040)  # 2COM,1/2 bias
CMD_B2C3      = const(0x048)  # 3COM,1/2 bias
CMD_B2C4      = const(0x050)  # 4COM,1/2 bias

* LCD 1/3 bias option
CMD_B3C2      = const(0x042)  # 2COM,1/3 bias
CMD_B3C3      = const(0x04A)  # 3COM,1/3 bias
CMD_B3C4      = const(0x052)  # 4COM,1/3 bias

* System clock Set
CMD_RC256K    = const(0x030)  # System clock source, on-chip RC oscillator
CMD_EXT256K   = const(0x038)  # System clock source, external clock source
CMD_XTAL32K   = const(0x028)  # System clock source, crystal oscillator

* Time base
CMD_TIMER_EN  = const(0x00C)  # Enable time base output
CMD_TIMER_DIS = const(0x008)  # Disable time base output
CMD_CLR_TIMER = const(0x018)  # Clear the contents of time base generator

* WDT set
CMD_WDT_DIS = const(0x00A)  # Disable WDT time-out flag output
CMD_WDT_EN  = const(0x00E)  # Enable WDT time-out flag output
CMD_CLR_WDT = const(0x01C)  # Clear the contents of WDT stage

* Sound output set
CMD_TONE2K  = const(0x0C0)  # Tone frequency, 2kHz
CMD_TONE4K  = const(0x080)  # Tone frequency, 4kHz
CMD_TONEON  = const(0x012)  # Turn on tone outputs
CMD_TONEOFF = const(0x010)  # Turn off tone outputs

* Time base/WDT clock output set
CMD_F1      = const(0x140)  # Time base/WDT clock output:1Hz | The WDT time-out flag after: 4s
CMD_F2      = const(0x142)  # Time base/WDT clock output:2Hz | The WDT time-out flag after: 2s
CMD_F4      = const(0x144)  # Time base/WDT clock output:4Hz | The WDT time-out flag after: 1s
CMD_F8      = const(0x146)  # Time base/WDT clock output:8Hz | The WDT time-out flag after: 1/2s
CMD_F16     = const(0x148)  # Time base/WDT clock output:16Hz | The WDT time-out flag after: 1/4s
CMD_F32     = const(0x14A)  # Time base/WDT clock output:32Hz | The WDT time-out flag after: 1/8s
CMD_F64     = const(0x14C)  # Time base/WDT clock output:64Hz | The WDT time-out flag after: 1/16s
CMD_F128    = const(0x14E)  # Time base/WDT clock output:128Hz | The WDT time-out flag after: 1/32s

* IRQ set
CMD_IRQ_DIS = const(0x100)  # Disable IRQ output
CMD_IRQ_EN  = const(0x110)  # Enable IRQ output

* Work mode set</BR>
CMD_TEST    # Test mode, user don't use</BR>
CMD_NORMAL  # Normal mode</BR>

  
  </BR></BR>



GDC03849
----
> GDC03849 是一款由大连佳显公司生产的液晶屏幕。详细信息请阅读 [GDC03849数据手册][2]。



### API

* **viewTemp(_gdcdata)**</BR>
*在温度区显示温度值*</BR>
  _gdcdata: 温度值（浮点数）</BR>
  ```python
  # 显示温度值为 25.34。
  viewTemp(25.34)
  ```
  
* **viewRH(_gdcdata)**</BR>
*在湿度区显示湿度值*</BR>
  _gdcdata: 温度值（浮点数）</BR>
  ```python
  # 显示湿度值为 93.43。
  viewRH(93.45)
  ```

* **LCDALLSHOW()**</BR>
*显示整片LCD所有字段*</BR>

* **LCDALLCLEAR()**</BR>
*清除整片LCD所有字段*</BR>

* **TEMPCLEAR()**</BR>
*清除温度区域（整行）所有字段显示*</BR>
  
* **RHCLEAR()**</BR></BR>
*清除湿度区域（整行）所有字段显示*</BR>

### 常量
* **NUMCODE_RH_HEX**</BR>
*以元组方式存储的湿度区单个字符的段码编码（16进制）*

* **NUMCODE_TEMP_HEX**</BR>
*以元组方式存储的温度区单个字符的段码编码（16进制）*


[]:http://www.holtek.com.cn