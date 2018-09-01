### 单个机械按钮
---
简介：
单个机械按键的驱动模块。


模块名称：keyboard

驱动名称：KEYBOARD

| 参数名称 | 参数类型 | 参数值 | 默认值 | 备注 |
| -- | -- | -- | -- | -- |
| \_btnKey | Pin | Pin
| \_tmBtn | Pin | Pin
| \_btnDef = 1 | int | 1/0 | 0 |
| even_djlong = None | project | None/evn_long | None | eg: def evn_long(con): |
| even_lj = None | project | None / evn_con | None | eg:def evn_con(con): |
| \_pull = None | project | "UP"/"DOWN"/"None" | None |



用法举例：

<code>
from keyboard import KEYBOARD

# 按键引脚
p = Pin('B3')

# 定时器,按键时钟使用
s = Timer(1)

# 声明按键对象，并设置事件
sw = KEYBOARD(p, s, 0, evn_long, evn_con, "UP")
</code>
