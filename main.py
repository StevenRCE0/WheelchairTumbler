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
# Robot.switchMode('joint_mode')
Robot.rotateJoints({1: 245, 2: 160})
# Robot.rotateJoints({2: 160})
sleep(5)

# Robot.trot(1)

Robot.switchTorque('disable')

closePort(portHandler)
