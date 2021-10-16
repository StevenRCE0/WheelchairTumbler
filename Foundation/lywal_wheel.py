import math
from lywal_trot import DEVICENAME
from device import *
from dynamixel_sdk import *  # Uses Dynamixel SDK library

# Control table address
ADDR_MX_CW                   = 6
ADDR_MX_CCW                  = 8
ADDR_MX_OFFSET              = 20
ADDR_MX_TORQUE_ENABLE       = 24         #Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION       = 30
ADDR_MX_MOVING_SPEED        = 32
ADDR_MX_PRESENT_POSITION    = 36
ADDR_MX_PRESENT_LOAD        = 40


# Protocol version
PROTOCOL_VERSION            = 1.0  # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID1                      = 1            #Dynamixel ID: 1
DXL_ID2                      = 2            # Dynamixel ID: 1
DXL_ID3                      = 3            # Dynamixel ID: 1
DXL_ID4                      = 4            #Dynamixel ID: 1
DXL_ID5                      = 5            # Dynamixel ID: 1
DXL_ID6                      = 6            # Dynamixel ID: 1
DXL_ID7                      = 7           #Dynamixel ID: 1
DXL_ID8                      = 8
# BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600
BAUDRATE = 115200 # Dynamixel default baudrate : 57600
DEVICENAME = device()

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
index = 0
#dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]  # Goal position

#开扭矩
def switch_torque(id_list, switch):
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

def switch_mode(id_list, mode_name):                                         #模式切换
    if mode_name == 'wheel_mode':
        for id in id_list:
            packetHandler.write2ByteTxRx(portHandler, id, ADDR_MX_CW, DXL_WHEEL_MODE_CW_VALUE)
            packetHandler.write2ByteTxRx(portHandler,id, ADDR_MX_CCW, DXL_WHEEL_MODE_CCW_VALUE)
            packetHandler.write2ByteTxRx(portHandler, id, ADDR_MX_OFFSET, 6000)
    elif mode_name == 'multi_mode' :
        for id in id_list:
            packetHandler.write2ByteTxRx(portHandler, PROTOCOL_VERSION, id, ADDR_MX_CW, DXL_MULTI_MODE_CW_VALUE)
            packetHandler.write2ByteTxRx(portHandler, PROTOCOL_VERSION, id, ADDR_MX_CCW, DXL_MULTI_MODE_CCW_VALUE)
            packetHandler.write2ByteTxRx(portHandler, PROTOCOL_VERSION, id, ADDR_MX_OFFSET, 6000)

if __name__ == '__main__':
    portHandler = PortHandler(DEVICENAME)
    packetHandler = PacketHandler(PROTOCOL_VERSION)
    openPort(portHandler)

    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):                                            #设置波特率
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        getch()
        quit()

    id_list = [i for i in range(1,9)]
    switch_torque(id_list,'enable')                              #开扭矩
    dt = 0.05
    switch_mode(id_list, 'wheel_mode')                            #设置模式
    for id in id_list:
        dxl=[]
        # Read Dynamixel#1 present position
        dxl1_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, id,
                                                                                        ADDR_MX_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        dxl.append(dxl1_present_position)
        print("[ID:%03d]  PresPos:%03d" % (id, dxl1_present_position))                         #输出电机当前位置
        # Change goal position
    # pipeline,align,network, class_names, class_colors,args,profile=darknet_video.model()
    # location,a=darknet_video.shibie(pipeline, align, network, class_names, class_colors, args, profile)
    # while location[0] == 0 and location[2]==0:
    #     location,a = darknet_video.shibie(pipeline, align, network, class_names, class_colors, args, profile)
    while 1:
        # c = int(input("Press any key to continue! (or press 0 to quit!)"))
        # print(c)
        # if c == 0:
        #     break
        # # 1和2控制一条腿
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler,  1,ADDR_MX_MOVING_SPEED, 1124)
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler,  2,ADDR_MX_MOVING_SPEED, 100)
        #3和4控制一条腿
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler,  3,ADDR_MX_MOVING_SPEED, 1124)
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler,  4,ADDR_MX_MOVING_SPEED, 100)
        #5和7控制一条腿
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler,  5,ADDR_MX_MOVING_SPEED, 100)
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler,  7,ADDR_MX_MOVING_SPEED, 1124)
        # #6和8控制一条腿
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler,  6,ADDR_MX_MOVING_SPEED, 100)
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler,  8,ADDR_MX_MOVING_SPEED, 1124)
        # location,a= darknet_video.shibie(pipeline, align, network, class_names, class_colors, args, profile)
        # while location[0] == 0 and location[2]==0:
        #     location,a = darknet_video.shibie(pipeline, align, network, class_names, class_colors, args, profile)
    switch_torque(id_list, "disable")                                  #关扭矩
    portHandler.closePort()                                            #关闭端口
