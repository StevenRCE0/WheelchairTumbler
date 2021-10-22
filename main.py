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

Robot.rotateJoints({1: -80, 2: -80, 3: -80, 4: -80, 5: -80, 7: -80, 6: -80, 8: -80})
sleep(1)
# Robot.setSpeed(speedDict)
Robot.positionZero = Robot.readPersentPosition()
Robot.trot(1)

Robot.switchTorque('disable')

closePort(portHandler)
