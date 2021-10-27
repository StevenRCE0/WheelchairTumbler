from time import sleep
from Foundation.behaviours import *
import Foundation.basis as basis

portHandler = PortHandler(basis.DEVICENAME)
packetHandler = PacketHandler(basis.PROTOCOL_VERSION)
openPort(portHandler)
setBaudRate(portHandler, basis.BAUDRATE)

id_list = [i for i in range(1, 9)]
Robot = Lywal(id_list, portHandler, packetHandler)

# 初始化动作
Robot.switchTorque('enable')
Robot.rotateServo(initializeRotationDict())
Robot.setSpeed(100)
Robot.rotatePositionZero()

# 整个俯卧撑
Robot.manipulateClaw(80, [1, 2, 3, 4])
Robot.manipulateClaw(-80, [1, 2, 3, 4])
Robot.manipulateClaw(80, [5, 6, 7, 8])
Robot.manipulateClaw(-80, [5, 6, 7, 8])
Robot.rotatePositionZero()

# 三足站立
Robot.rotateGroup(-10, [3, 4])
Robot.rotateGroup(90, [6, 8])
Robot.rotateGroup(-20, [5, 7])
Robot.manipulateClaw(40, [3, 4, 5, 7])
sleep(0.2)
Robot.manipulateClaw(50, [1, 2])
Robot.manipulateClaw(30, [6, 8])
Robot.rotateGroup(-60, [6, 8])
sleep(0.2)
Robot.manipulateClaw(20, [3, 4, 5, 7])
Robot.manipulateClaw(20, [6, 8])
Robot.manipulateClaw(20, [3, 4, 5, 7])
Robot.manipulateClaw(-50, [1, 2])

print('potential')
Robot.rotatePositionZero([1])
# 手动作
Robot.rotateGroup(180, [1, 2])
Robot.manipulateClaw(70, [1, 2])
Robot.rotateGroup(60, [1, 2])
Robot.rotateGroup(-60, [1, 2])


Robot.manipulateClaw(-70, [1, 2])
Robot.rotateGroup(-180, [1, 2])
Robot.manipulateClaw(-80, [3, 4, 5, 7])
Robot.manipulateClaw(-50, [6, 8])



# 复位
print('resr', Robot.wheelState)
print('resrt', Robot.clawState)

Robot.rotatePositionZero()
print('resr', Robot.wheelState)
print('resrt', Robot.clawState)
sleep(1)

# 步行
Robot.trot(repetitive=3)
sleep(3)

# 退出 - bogus!
Robot.switchTorque('quit')

# ???
sleep(1)
Robot.rotateGroup(360, [5, 6, 7, 8])
sleep(2)
Robot.rotatePositionZero()
sleep(1)
Robot.manipulateClaw(80, [5, 6, 7, 8])
sleep(1)
Robot.rotateGroup(-60, [5, 6, 7, 8])
sleep(1)
Robot.setSpeed(100)
Robot.rotateGroup(-180, [1, 2, 3, 4])
sleep(1)
Robot.manipulateClaw(80, [1, 2, 3, 4])
sleep(0.5)
Robot.rotateGroup(180, [1, 2, 3, 4])
Robot.rotateGroup(50, [5, 6, 7, 8])

sleep(1)

Robot.switchTorque('disable')
closePort(portHandler)
