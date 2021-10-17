from Foundation.device import *
from Foundation.basis import *

from dynamixel_sdk import *  # Uses Dynamixel SDK library

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
    setBaudRate(portHandler, BAUDRATE)

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
        c = int(getch())
        print(c)
        if c == 0:
            break
        # 1和2控制一条腿
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler,  1,ADDR_MX_MOVING_SPEED, 1124)
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler,  2,ADDR_MX_MOVING_SPEED, 100)
        # 3和4控制一条腿
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler,  3,ADDR_MX_MOVING_SPEED, 1124)
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler,  4,ADDR_MX_MOVING_SPEED, 100)
        # 5和7控制一条腿
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler,  5,ADDR_MX_MOVING_SPEED, 100)
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler,  7,ADDR_MX_MOVING_SPEED, 1124)
        # 6和8控制一条腿
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler,  6,ADDR_MX_MOVING_SPEED, 100)
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler,  8,ADDR_MX_MOVING_SPEED, 1124)
        # location,a= darknet_video.shibie(pipeline, align, network, class_names, class_colors, args, profile)
        # while location[0] == 0 and location[2]==0:
        #     location,a = darknet_video.shibie(pipeline, align, network, class_names, class_colors, args, profile)
    switch_torque(id_list, "disable")                                  #关扭矩
    portHandler.closePort()                                            #关闭端口
