import math
import Foundation.init as init
from Foundation.device import *
from Foundation.basis import *
from Foundation.behaviours import *

from dynamixel_sdk import *

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)
openPort(portHandler)
setBaudRate(portHandler, BAUDRATE)

id_list = [i for i in range(1,9)]
Theta = [0, 0, 0, 0, 0, 0, 0, 0]

Robot = Lywal(id_list, portHandler, packetHandler)

Robot.switchTorque('enable')
detT = 0.02
Robot.switchMode('multi_mode')
dxl= Robot.readPersentPosition()
while 1:
    print("Press any key to continue! (or press 0 to quit!)")

    if getch() == 0:
        break
    N=0
    NUM = 1000 # ???
    T=2.0
    desth=init.init(T,detT)
    t0 = time.time()
    while N<500 and time.time()-t0<10:
        t= time.time()-t0
        if t>N*detT:
            # id=1,2
            Index1=(N)%(T/detT)
            Index1 = math.floor(Index1)
            if Index1==40:
                Index1=0
            
            Theta[0]=int(4096/360*30+dxl[0]+desth[0][Index1]*4096/360)
            Robot.writeDataToServo(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, 1, Theta[0])

            Theta[1]=int(4096/360*210+dxl[1]-desth[1][Index1]*4096/360)
            Robot.writeDataToServo(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, 2, Theta[1])

            # #2,3
            # Theta[2] = int(4096 / 360 * 30  + dxl[2] + desth[2][Index1] * 4096 / 360)
            # Theta[3] = int(4096 / 360 * 210 + dxl[3] - desth[3][Index1] * 4096 / 360)
            # #4,6
            # Theta[6] = int(4096 / 360 * 30  + dxl[6] + desth[6][Index1] * 4096 / 360)
            # Theta[4] = int(4096 / 360 * 210 + dxl[4] - desth[4][Index1] * 4096 / 360)

            #5,7
            # Theta[5] = int(4096 / 360 * 30  + dxl[5] + desth[5][Index1] * 4096 / 360)
            # Theta[7] = int(4096 / 360 * 210 + dxl[7] - desth[7][Index1] * 4096 / 360)

            # Robot.writeData(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta)
            N = N + 1
        # for i in range(len(id_list)):
        #     Theta[i]=dxl[i]
        #     write_data(id_list, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta)
        # x=0
        # time.sleep(1)
        # t0 = time.time()
        # # dxl=readpersentposition(id_list)
        # id=[1,2]
        # Theta1 = [1, 2]
        # dxl=readpersentposition(id)
        # while x<121:
        #     t = time.time() - t0
        #     if t> x *detT:
        #         for i in [0]:
        #             Theta[i] = int(dxl[0] - 4096 / 360 *1* x)1
        #         for i in [1]:
        #             Theta[i] = int(dxl[1] + 4096 / 360 *1* x)
        #         x = x + 1
        #         write_data(id, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta1)
        # time.sleep(1)
        # # id=[1,2]
        # dxl=readpersentposition(id)
        # # Theta1=[1,2]
        # Theta1[0]=int(4096/360*15+dxl[0])
        # Theta1[1]=int(4096/360*15+dxl[1])
        # write_data(id, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta1)
        # time.sleep(1)
        # t0 = time.time()
        # while x<50:
        #     t = time.time() - t0
        #     if t> x *detT:
        #         for i in [0]:#[0,2,6,7]:
        #             Theta1[i] = int(dxl[0] -4096 / 360 *1* x)
        #         for i in [1]:#[1,3,4,5]:
        #             Theta1[i] = int(dxl[1] +4096 / 360 *1* x)
        #         x = x + 1
        #         write_data(id, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta1)


Robot.switchTorque("disable")
closePort(portHandler)
