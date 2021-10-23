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
Robot.switchMode('multi_mode')
print(Robot.initialPositions)
# speedDict = {}
# for index in range(8):
#     speedDict[index + 1] = 50
# print(speedDict)
# Robot.setSpeed(speedDict)
sleep(5)
Robot.rotateJoints(initializeRotationDict())
sleep(1)
Robot.positionZero = Robot.readPersentPosition()
print("pos0 = " + str(Robot.positionZero))
# Robot.switchMode('multi_mode', [1, 2, 3, 4])
Robot.switchMode('wheel_mode')
# Robot.trot(repetitive = 1, servos = [1, 2, 3, 4])
# Robot.trot(repetitive = 1, servos = [1, 2, 3, 4])
Robot.drive([10, 10, 10, 10])
sleep(1)
Robot.drive([0, 0, 0, 0])
Robot.switchMode('multi_mode')
Robot.rotateToZero()
sleep(20)
Robot.trot()

Robot.switchTorque('disable')

closePort(portHandler)
