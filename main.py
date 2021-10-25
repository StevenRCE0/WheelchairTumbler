from time import sleep

from dynamixel_sdk import robotis_def
from Foundation.behaviours import *
import Foundation.basis as basis

portHandler = PortHandler(basis.DEVICENAME)
packetHandler = PacketHandler(basis.PROTOCOL_VERSION)
openPort(portHandler)
setBaudRate(portHandler, basis.BAUDRATE)

id_list = [i for i in range(1, 9)]
Robot = Lywal(id_list, portHandler, packetHandler)

Robot.switchTorque('enable')
Robot.switchMode('multi_mode')
print(Robot.initialPositions)
# sleep(5)
Robot.rotateJoints(initializeRotationDict())
sleep(1)
Robot.positionZero = Robot.readPersentPosition()
print("pos0 = " + str(Robot.positionZero))
sleep(2)
# Robot.switchMode('multi_mode', [1, 2, 3, 4])
# Robot.switchMode('wheel_mode')
# Robot.trot(repetitive = 1, servos = [1, 2, 3, 4])
# Robot.drive([100, 100, 100, 100])
# sleep(1)
# Robot.drive([-100, -100, -100, -100])
# sleep(1)
# speedDict = {1: 80, 2: 80, 3: 80, 4: 80, 5: 80, 6: 80, 7: 80, 8: 80}
# Robot.setSpeed(speedDict)
# Robot.rotateToZero()
# sleep(20)

Robot.deltaT = 0.01
Robot.rotateGroup(30, [1, 2])
Robot.rotateGroup(-30, [1, 2])
Robot.rotateToZero([1, 2])
sleep(2)
Robot.manipulateClaw(40, [3, 4, 5, 7])
Robot.rotateGroup(-10, [3, 4])
Robot.manipulateClaw(50, [1, 2])
Robot.manipulateClaw(30, [6, 8])
sleep(2)
Robot.manipulateClaw(40, [3, 4, 5, 7])
Robot.manipulateClaw(40, [6, 8])
sleep(2)
Robot.manipulateClaw(-50, [1, 2])
sleep(4)
Robot.rotateGroup(360, [1, 2])
Robot.manipulateClaw(20, [1, 2])
Robot.rotateGroup(45, [1, 2])
Robot.rotateGroup(-45, [1, 2])
Robot.manipulateClaw(-20, [1, 2])

sleep(3)
Robot.rotateToZero()

sleep(5)

Robot.trot(repetitive= 3)
Robot.rotateToZero()

Robot.switchMode('wheel_mode')
Robot.drive([70, -70, 70, -70])
sleep(5)
Robot.switchTorque('quit')


sleep(1)
Robot.rotateGroup(360, [5, 6, 7, 8])
sleep(2)
Robot.rotateToZero()
sleep(1)
# Robot.claw()
Robot.manipulateClaw(80, [5, 6, 7, 8])
sleep(1)
Robot.rotateGroup(-60, [5, 6, 7, 8])
sleep(1)
Robot.deltaT = 0
Robot.rotateGroup(-180, [1, 2, 3, 4])
sleep(1)
Robot.manipulateClaw(80, [1, 2, 3, 4])
sleep(0.5)
Robot.rotateGroup(180, [1, 2, 3, 4])
Robot.rotateGroup(50, [5, 6, 7, 8])

# Robot.deltaT = 0.02
sleep(1)

# Robot.trot()

Robot.switchTorque('disable')

closePort(portHandler)
