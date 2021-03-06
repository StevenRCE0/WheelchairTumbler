# WheelchairTumbler Foundation
这是基于先前各 Lywal 团队开发的代码编写的 Lywal 控制接口。

## Behaviours
该程序用于控制 Lywal 的各种动作行为，包含一个 Lywal 类，支持如下变量定义和方法：

### 实例化
**实例化需提供**
> **li_list**: list

Dynamixel 伺服机的 ID 列表，有指定顺序。在 Basis 中有定义。

> **portHandler**: class

PortHandler 类，在 Dynamixel SDK 中提供。其实例化需提供 DEVICENAME，DEVICENAME 在 Device 中有定义。

> **packetHandler**: class

packetHandler 类，在 Dynamixel SDK 中提供。其实例化需提供 PROTOCOL_VERSION，PROTOCOL_VERSION 在 Basis 中有定义。


### deltaT
采样模式中的采样间隔，以秒为单位。当目标位置按照间隔生成时，数值越小运动速度越快。


### switchTorque
根据输入切换对应伺服机的扭矩模式。

**参数**
> **switch**: str ('enable' | 'disable' | 'quit')

enable 打开扭矩，disable 关闭扭矩，quit 用于关闭扭矩并异常退出。

> **servoArray**: \*list

可选，默认为所有伺服机。需要切换扭矩模式的伺服机 ID。


### setSpeed
设置采样模式下的运动速度，通过计算并修改适当的 deltaT 来实现。

**参数**
> **speedPercentage**: float | int

设置速度，范围为0~100。


### readPresentPosition
读取所有伺服机的当前位置。

**参数**
> **targetServo**: \*list (keyword)

可选，目标伺服机 ID，默认为所有伺服机，按给定顺序输出。

> **targetDict**: \*bool (keyword)

可选，给定 true 时以伺服机 ID 作为 key，位置码作为 value 输出  dict

> **degree**: \*bool (keyword)

可选，给定 true 时输出角度制的位置。


### writeData
向伺服机写入数据。

**参数**
> **adr**: int

写入地址位置。

> **adr_len**: int

写入地址长度。

> **dataPairs**: dict

以写入伺服机 ID 作为 key，目标值作为 value 的 dict。


### rotateServo
旋转指定伺服机，角度制。

**参数**
> **anglePairs**: dict

以写入伺服机 ID 作为 key，角度作为 value 的 dict。


### rotateGroup
旋转轮子（伺服机组），角度制。

**参数**
> **angle**: int

旋转角度。

> **servoList**: \*list

可选，旋转的伺服机 ID，默认为所有。例如：旋转某轮子时需填写对应两个伺服机的 ID。


### manipulateClaw
操作爪模式，角度制。

**参数**
> **angle**: int

张开角度。

> **servoList**: list

旋转的伺服机 ID。例如：张开某轮子时需填写对应两个伺服机的 ID。


### fourWheelDrive
以采样模式四轮同步驱动行驶，输入圈数。**会受到多圈模式的角度限制，不能大幅移动。**

**参数**
> **rotation**: int

转动的圈数。

> **directionArray**: list

需要转动的伺服机的方向。“1”为正，“-1”为负。也可以用作倍率。建议将同一轮子对应的伺服机方向设为一致的。


### manuallyResetTrot
手动从爬行状态重置。数值仅为经验结果。


### trot
爬行模式。

**参数**
> **repetitive**: \*int (keyword)

可选，重复次数，默认为1。

> **servos**: \*list (keyword)

可选，步行伺服机的 ID 列表，默认为全部。


### clawGrab
夹起木棒的预设动作。


### rotatePositionZero
根据操作历史重置电机位置。**仅对采样模式下的操作（爬行除外）有效。切换模式会失效。**

**参数**
> **servoGroups**: \*list

可选，重置轮子的编号，默认为全部。范围为1~4。


## Device
运行终端的设备配置信息。

### device
根据当前运行系统输出串口板的设备名，可能需要根据情况自行修改。


### openPort
封装的打开端口函数，有自动中止功能。

**参数**
> **definedPortHandler**: Protocol1PacketHandler | Protocol2PacketHandler

提供根据 Dynamixel SDK 创建的 portHandler 实例。


### closePort
封装的关闭端口函数。

**参数**
> **definedPortHandler**: Protocol1PacketHandler | Protocol2PacketHandler

提供根据 Dynamixel SDK 创建的 portHandler 实例。


### setBaudRate
设定波特率。

**参数**
> **definedPortHandler**: Protocol1PacketHandler | Protocol2PacketHandler

提供根据 Dynamixel SDK 创建的 portHandler 实例。

> **targetBaudRate**: int

提供目标波特率，通常使用 Basis 中的定义。

### getch
根据当前运行系统和交互模式提供逐步调试所需的获取输入字符函数。当不在交互模式中调取时默认返回 'c'。


## Basis
开头为 Dynamixel 有关参数的默认定义，详情请查阅 [Dynamixel 相关文档](https://emanual.robotis.com/docs/en/dxl/mx/mx-28)。

之后含有一些内部调用的小工具，非常简单，应该不用说明。


## Script Toolbox
若干脚本工具

### setup.sh
初始化环境脚本，会按照 requirements.txt 在本地安装运行所需的依赖库。

### run.sh
按照目录结构将项目跟文件夹上传到 Lywal 主机 (会忽略 Instructions 文件夹)。随后自动在 Lywal 主机上运行 nano.sh 来执行程序。

### nano.sh
在 Lywal 上运行主程序的脚本，会按照给定的 "密码" 提权运行。


## Instructions
电机控制介绍和视觉部分介绍，先前开发团队提供的指导资料。
