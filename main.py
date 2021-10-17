from Foundation.behaviours import *
from Foundation.basis import *

print(DEVICENAME)
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)
openPort(portHandler)
setBaudRate(portHandler, BAUDRATE)

id_list = [i for i in range(1, 9)]
powerArray = [20, 5, 5, 5]
Robot = Lywal(id_list, portHandler, packetHandler)
Robot.switch_torque('enable')
Robot.switch_mode('wheel_mode')
Robot.moveBot(powerArray)
time.sleep(5)
Robot.switch_torque('disable')

closePort(portHandler)