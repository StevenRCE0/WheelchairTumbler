from time import sleep
from Foundation.behaviours import *
from Foundation.basis import *

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)
openPort(portHandler)
setBaudRate(portHandler, BAUDRATE)

id_list = [i for i in range(1, 9)]
Robot = Lywal(id_list, portHandler, packetHandler)

Robot.switchTorque('enable')
# Robot.switchMode('wheel_mode')
# Robot.drive([4, 4, 4, 4])
# time.sleep(5)
# Robot.drive([0, 0, 0, 0])
Robot.switchMode('multi_mode')
print(Robot.initialPositions)
# speedDict = {}
# for index in range(8):
#     speedDict[index + 1] = 50
# print(speedDict)
# Robot.setSpeed(speedDict)

Robot.rotateJoints(initializeRotationDict())
sleep(1)
Robot.positionZero = Robot.readPersentPosition()
Robot.rotateToZero()
Robot.trot(repetitive = 1)
Robot.rotateToZero()

Robot.switchTorque('disable')

closePort(portHandler)
