import math
from dynamixel_sdk import *  # Uses Dynamixel SDK library
import time
import init
import device
# Control table address
# Control table address
ADDR_MX_CW                   = 6
ADDR_MX_CCW                  = 8
ADDR_MX_OFFSET              = 20
ADDR_MX_TORQUE_ENABLE       = 24         #Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION       = 30
ADDR_MX_MOVING_SPEED        = 32
ADDR_MX_PRESENT_POSITION    = 36
ADDR_MX_PRESENT_LOAD        = 40

LEN_MX_GOAL_POSITION        = 4
LEN_MX_PRESENT_LOAD         = 4


# Protocol version
PROTOCOL_VERSION            = 1.0  # See which protocol version is used in the Dynamixel

# BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600
BAUDRATE = 115200 # Dynamixel default baudrate : 57600
DEVICENAME = device.device()

TORQUE_ENABLE = 1  # Value for enabling the torque
TORQUE_DISABLE = 0  # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE = 100  # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE = 900  # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 10  # Dynamixel moving status threshold
# DXL_MOVING_STATUS_THRESHOLD = 1  # Dynamixel moving status threshold

# mode
DXL_MULTI_MODE_CW_VALUE = 4095
DXL_WHEEL_MODE_CW_VALUE = 0
DXL_MULTI_MODE_CCW_VALUE = 4095
DXL_WHEEL_MODE_CCW_VALUE = 0
VELOCITY_MODE = 1
POSITION_MODE = 3
#dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]  # Goal position
def switch_torque(id_list, switch):                                                                 #开扭矩
    if switch == 'enable':
        for id in id_list:
            dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, id, ADDR_MX_TORQUE_ENABLE,
                                                                      TORQUE_ENABLE)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))
            else:
                print("Dynamixel#%d has been successfully connected" % id)
    elif switch == 'disable':
        for id in id_list:
            dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, id, ADDR_MX_TORQUE_ENABLE,
                                                                      TORQUE_DISABLE)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("parameters of switch_torque wrong!")
    return

def switch_mode(id_list, mode_name):                                         #模式切换`Q
    if mode_name == 'wheel_mode':
        for id in id_list:
            packetHandler.write2ByteTxRx(portHandler, id, ADDR_MX_CW, DXL_WHEEL_MODE_CW_VALUE)
            packetHandler.write2ByteTxRx(portHandler,id, ADDR_MX_CCW, DXL_WHEEL_MODE_CCW_VALUE)
            packetHandler.write2ByteTxRx(portHandler, id, ADDR_MX_OFFSET, 6000)
    elif mode_name == 'multi_mode' :
        for id in id_list:
            packetHandler.write2ByteTxRx(portHandler, id, ADDR_MX_CW, DXL_MULTI_MODE_CW_VALUE)
            packetHandler.write2ByteTxRx(portHandler,id, ADDR_MX_CCW, DXL_MULTI_MODE_CCW_VALUE)
            packetHandler.write2ByteTxRx(portHandler,id, ADDR_MX_OFFSET, 6000)
def readpersentposition(id_list):
    dxl=[]
    for id in id_list:
        # Read Dynamixel#1 present position
        dxl1_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, id,
                                                                                        ADDR_MX_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d]  PresPos:%03d" % (id, dxl1_present_position))
        dxl.append(dxl1_present_position)
    return dxl

def write_data(id_list, adr, adr_len, data):                 #把目标位置写进电机
    groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, adr, adr_len)
    param_goal_positions = []
    for i in range(len(id_list)):
        param_goal_positions.append([DXL_LOBYTE(DXL_LOWORD(data[i])),DXL_HIBYTE(DXL_LOWORD(data[i])),DXL_LOBYTE(DXL_HIWORD(data[i])),DXL_HIBYTE(DXL_HIWORD(data[i]))])
    for i in range(len(id_list)):
        dxl_addparam_result = groupSyncWrite.addParam(id_list[i],param_goal_positions[i])
        if dxl_addparam_result != True:
            print("[ID:%03d] groupSyncWrite addparam failed" % id_list[i])
            quit()
    dxl_comm_result = groupSyncWrite.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

    groupSyncWrite.clearParam()
    return
if __name__ == '__main__':
    portHandler = PortHandler(DEVICENAME)
    packetHandler = PacketHandler(PROTOCOL_VERSION)

    # Open port
    if portHandler.openPort():                                                     #开启端口
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
     #   getch()
        quit()

    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):                                            #设置波特率
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
     #   getch()
        quit()

    id_list=[i for i in range(1,9)]
    Theta= [i for i in range(1, 9)]
    id = [1,2,3,4]
    Theta1 = [1,2,3,4]
    detT = 0.05
    switch_mode(id_list, 'multi_mode')
    switch_torque(id_list,'enable') #设置模式
    dxl=readpersentposition(id_list)

    while 1:
        c = int(input("Press any key to continue! (or press 0 to quit!)"))
        print(c)
        if c == 0:
            break
        # N=0
        # NUM = 1000
        # T=2.0
        # desth=init.init(T,detT)                                  #得到目标角度
        # t0 = time.time()
        # Theta = [i for i in range(1,9)]
        # while N<NUM and time.time()-t0<10:                        #足模式行走
        #     t= time.time()-t0
        #     if t>N*detT:
        #         # id=1,2 控制第一条腿
        #         Index1=(N)%(T/detT)
        #         Index1 = math.floor(Index1)
        #         if Index1==40:
        #             Index1=0
        #         Theta[0]=int(4096/360*30+dxl[0]+desth[0][Index1]*4096/360)
        #         Theta[1]=int(4096/360*210+dxl[1]-desth[1][Index1]*4096/360)
        #         # #2,3控制一条腿
        #         Theta[2]=int(4096/360*30+dxl[2]+desth[2][Index1]*4096/360)
        #         Theta[3] = int(4096 / 360 * 210+dxl[3]-desth[3][Index1] * 4096 / 360)
        #         # #4,6控制
        #         Theta[6] = int(4096 / 360 * 30 + dxl[6] + desth[6][Index1] * 4096 / 360)
        #         Theta[4] = int(4096 / 360 * 210 + dxl[4] - desth[4][Index1] * 4096 / 360)
        #
        #         #5,7控制
        #         Theta[5] = int(4096 / 360 *30+ dxl[5] +desth[5][Index1] * 4096 / 360)
        #         Theta[7] = int(4096 / 360 * 210 + dxl[7] -desth[7][Index1] * 4096 / 360)
        #         write_data(id_list,ADDR_MX_GOAL_POSITION ,LEN_MX_GOAL_POSITION,Theta)
        #         N = N + 1
        # for i in range(len(id_list)):                              #合成轮子
        #     Theta[i]=dxl[i]
        #     write_data(id_list, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta)
        x=0
        t0 = time.time()                             #向前滚
        dxl=readpersentposition(id_list)
        while x<121:
            t = time.time() - t0
            if t> x *detT:
                for i in [0,2,6,7]:
                    Theta[i] = int(dxl[i] - 4096 / 360 *1*x)
                for i in [1,3,4,5]:
                    Theta[i] = int(dxl[i] + 4096 / 360 *1*x)
                x = x + 1
                write_data(id_list, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta)
        time.sleep(1)                         #前轮张开一定角度
        # id=[1,2]
        dxl=readpersentposition(id)
        # Theta1=[1,2]
        for i in range(len(Theta1)):
            Theta1[i] = int(4096 / 360 * 15+ dxl[i])

        write_data(id, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta1)
        time.sleep(1)                            #向前滚一定角度
        t0 = time.time()
        x=0
        dxl = readpersentposition(id_list)
        while x<60:
            t = time.time() - t0
            if t> x *detT:
                for i in [0,2,6,7]:#[0,2,6,7]:
                    Theta[i] = int(dxl[i] -4096 / 360 *1*x)
                for i in [1,3,4,5]:#[1,3,4,5]:
                    Theta[i] = int(dxl[i] +4096 / 360 *1*x)
                x = x + 1
                write_data(id_list, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta)
        dxl = readpersentposition(id)
        time.sleep(1)                                   #前轮夹起棍子
        dxl = readpersentposition(id)
        for i in range(len(Theta1)):
            Theta1[i] = int(-4096 / 360 * 6+ dxl[i])
        write_data(id, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta1)
        x=0
        time.sleep(1)                                   #向后转
        dxl = readpersentposition(id_list)
        t0 = time.time()
        while x<240:
            t = time.time() - t0
            if t> x *detT:
                for i in [0,2,6,7]:#[0,2,6,7]:
                    Theta[i] = int(dxl[i] +4096 / 360 *1* x)
                for i in [1,3,4,5]:#[1,3,4,5]:
                    Theta[i] = int(dxl[i] -4096 / 360 *1* x)
                x = x + 1
                write_data(id_list, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta)

    switch_torque(id_list, "disable")  # 关扭矩
    portHandler.closePort()