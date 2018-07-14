[:uk:English](./README.md)

3Wire-HT1621B-GDC03849
====
![Frame diagram](./images/ht1621b_gdc.png)
> 3Wire-HT1621B-GDC03849 为ht1621b作为驱动芯片的GDC03849液晶驱动模块。驱动芯片与主CPU为3+CS总线通讯方式进行数据交换。

* 功能符号(标志字)</BR>
名称 | 描述
--- | ---
FLAG_CMD | 命令
FLAG_READ | 只读RAM
FLAG_WRITE | 只写RAM
FLAG_MODIFY | 读和写RAM(即修改RAM)READ-MODIFY-WRITE


HT1621B
----
> HT1621B 一款由台湾和泰芯片厂生产制作的LCD驱动芯片。详细资料请阅读 [HT1621B数据手册][1]


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
*芯片功能与参数初始化。*

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
*以列表方式存储的湿度区单个字符的段码编码（16进制）*

* **NUMCODE_TEMP_HEX**</BR>
*以列表方式存储的温度区单个字符的段码编码（16进制）*
