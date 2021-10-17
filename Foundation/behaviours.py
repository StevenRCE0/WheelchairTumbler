import math
import numpy as np
import Foundation.init as init
from Foundation.device import *
from Foundation.basis import *

from dynamixel_sdk import *  # Uses Dynamixel SDK library


class Lywal:
    def __init__(self, id_list, portHandler, packetHandler):
        self.id_list = id_list
        self.portHandler = portHandler
        self.packetHandler = packetHandler

    #开扭矩
    def switch_torque(self, switch):
        if switch == 'enable':
            for id in self.id_list:
                dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, id, ADDR_MX_TORQUE_ENABLE,
                                                                        TORQUE_ENABLE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("Dynamixel#%d has been successfully connected" % id)
        elif switch == 'disable':
            for id in self.id_list:
                dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, id, ADDR_MX_TORQUE_ENABLE,
                                                                        TORQUE_DISABLE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("parameters of switch_torque wrong!")
        return

    # 模式切换
    def switch_mode(self, mode_name):
        if mode_name == 'wheel_mode':
            for id in self.id_list:
                self.packetHandler.write2ByteTxRx(self.portHandler, id, ADDR_MX_CW, DXL_WHEEL_MODE_CW_VALUE)
                self.packetHandler.write2ByteTxRx(self.portHandler,id, ADDR_MX_CCW, DXL_WHEEL_MODE_CCW_VALUE)
                self.packetHandler.write2ByteTxRx(self.portHandler, id, ADDR_MX_OFFSET, 6000)
        elif mode_name == 'multi_mode' :
            for id in self.id_list:
                self.packetHandler.write2ByteTxRx(self.portHandler, id, ADDR_MX_CW, DXL_MULTI_MODE_CW_VALUE)
                self.packetHandler.write2ByteTxRx(self.portHandler, id, ADDR_MX_CCW, DXL_MULTI_MODE_CCW_VALUE)
                self.packetHandler.write2ByteTxRx(self.portHandler,id, ADDR_MX_OFFSET, 6000)

    def readpersentposition(self):
        dxl=[]
        for id in self.id_list:
            # Read Dynamixel#1 present position
            dxl1_present_position, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, id,
                                                                                            ADDR_MX_PRESENT_POSITION)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            print("[ID:%03d]  PresPos:%03d" % (id, dxl1_present_position))
            dxl.append(dxl1_present_position)
        return dxl

    def write_data(self, adr, adr_len, data):                 #把目标位置写进电机
        groupSyncWrite = GroupSyncWrite(self.portHandler, self.packetHandler, adr, adr_len)
        param_goal_positions = []
        for i in range(len(self.id_list)):
            param_goal_positions.append([DXL_LOBYTE(DXL_LOWORD(data[i])),DXL_HIBYTE(DXL_LOWORD(data[i])),DXL_LOBYTE(DXL_HIWORD(data[i])),DXL_HIBYTE(DXL_HIWORD(data[i]))])
        for i in range(len(self.id_list)):
            dxl_addparam_result = groupSyncWrite.addParam(self.id_list[i],param_goal_positions[i])
            if dxl_addparam_result != True:
                print("[ID:%03d] groupSyncWrite addparam failed" % self.id_list[i])
                quit()
        dxl_comm_result = groupSyncWrite.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))

        groupSyncWrite.clearParam()
        return

    def moveBot(self, powerArray:list):
        def constructPower(power, servoIndex):
            multiplied = clamp(1024 * power // 100, 0, 1023)
            if servoIndex == 0:
                return 1024 + multiplied
            else: 
                return multiplied - 1
        if len(powerArray) != 4:
            print("expecting 4 groups of servo. ")
            return

        servoMap = {1:1, 2:2, 3:3, 4:4, 5:5, 6:7, 7:6, 8:8}
        for groupIndex in range(0, len(powerArray)):
            self.packetHandler.write2ByteTxRx(self.portHandler, servoMap[groupIndex * 2 + 1], ADDR_MX_MOVING_SPEED, constructPower(powerArray[groupIndex], 0))
            self.packetHandler.write2ByteTxRx(self.portHandler, servoMap[groupIndex * 2 + 2], ADDR_MX_MOVING_SPEED, constructPower(powerArray[groupIndex], 1))
