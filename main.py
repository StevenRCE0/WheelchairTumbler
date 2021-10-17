from Foundation.behaviours import *
from Foundation.basis import *

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)
openPort(portHandler)
setBaudRate(portHandler, BAUDRATE)

id_list = [i for i in range(1, 9)]
powerArray = [2, 2, 2, 2]
Robot = Lywal(id_list, portHandler, packetHandler)
Robot.switchTorque('enable')
Robot.switchMode('wheel_mode')
Robot.drive(powerArray)
time.sleep(5)
Robot.switchTorque('disable')

closePort(portHandler)
