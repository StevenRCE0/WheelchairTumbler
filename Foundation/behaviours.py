import math
import numpy as np
import Foundation.init as init
from Foundation.device import *
from Foundation.basis import *

from dynamixel_sdk import *

class Lywal:

    def __init__(self, id_list:list, portHandler, packetHandler):
        self.id_list = id_list
        self.portHandler = portHandler
        self.packetHandler = packetHandler

    def switchTorque(self, switch:str):
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

    def switchMode(self, mode_name:str):
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

    def readPersentPosition(self):
        dxl=[]
        for id in self.id_list:
            # Read Dynamixel present position
            dxl1_present_position, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, id,
                                                                                            ADDR_MX_PRESENT_POSITION)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            print("[ID:%03d]  PresPos:%03d" % (id, dxl1_present_position))
            dxl.append(dxl1_present_position)
        return dxl

    def writeData(self, adr, adr_len, data):
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
    
    def writeDataToServo(self, adr, adr_len, servoID, position):
        groupSyncWrite = GroupSyncWrite(self.portHandler, self.packetHandler, adr, adr_len)
        dxl_addparam_result = groupSyncWrite.addParam(servoID, [DXL_LOBYTE(DXL_LOWORD(position)),DXL_HIBYTE(DXL_LOWORD(position)),DXL_LOBYTE(DXL_HIWORD(position)),DXL_HIBYTE(DXL_HIWORD(position))])
        if dxl_addparam_result != True:
            print("[ID:%03d] groupSyncWrite addparam failed" % servoID)
            quit()
        dxl_comm_result = groupSyncWrite.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))

        groupSyncWrite.clearParam()

    def drive(self, powerArray:list):
        def constructPower(power, servoIndex):
            rotationFlag = (servoIndex == 0)
            if power > 0:
                rotationFlag = not rotationFlag
            power = abs(power)
            multiplied = clamp(1024 * power // 100, 0, 1023)
            if rotationFlag == 0:
                return 1024 + multiplied
            else: 
                return multiplied
        if len(powerArray) != 4:
            print("expecting 4 groups of servo. ")
            return

        for groupIndex in range(0, len(powerArray)):
            self.packetHandler.write2ByteTxRx(self.portHandler, servoMap[groupIndex * 2 + 1], ADDR_MX_MOVING_SPEED, constructPower(powerArray[groupIndex], 0))
            self.packetHandler.write2ByteTxRx(self.portHandler, servoMap[groupIndex * 2 + 2], ADDR_MX_MOVING_SPEED, constructPower(powerArray[groupIndex], 1))

    def trot(self, *repetitive):
        destList = []
        repetitiveSet: int = 0
        if len(repetitive) == 0 or repetitive[0] <= 0:
            repetitiveSet = 1
        else:
            repetitiveSet = repetitive[0]

        for occurrence in range(0, repetitiveSet):
            runCount, desiredCount = 0, 500
            T, detT = 1000, 2.0, 0.2
            startTime  = time.time()
            desth = init.init(T, detT)
            dxl = self.readPersentPosition()

            while runCount < desiredCount and time.time() - startTime < 10:
                currentStartTime = time.time() - startTime
                if currentStartTime > runCount * detT:
                    # Debugging for servo #1 & #2
                    destIndex = int(math.floor((runCount) % (T / detT)))
                    if destIndex == 40:
                        destIndex = 0
                    
                    # Questionable dxl postion in test environment
                    destList = [
                        degToPositionalCode(desth[0][destIndex]  + 30)  + dxl[0],
                        degToPositionalCode(-desth[1][destIndex] + 210) + dxl[1],
                        degToPositionalCode(desth[2][destIndex]  + 30)  + dxl[2],
                        degToPositionalCode(-desth[3][destIndex] + 210) + dxl[3],
                        degToPositionalCode(-desth[4][destIndex] + 210) + dxl[4],
                        degToPositionalCode(desth[5][destIndex]  + 30)  + dxl[5],
                        degToPositionalCode(desth[6][destIndex]  + 30)  + dxl[6],
                        degToPositionalCode(-desth[7][destIndex] + 210) + dxl[7]
                    ]

                    self.writeDataToServo(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, 1, destList[0])
                    self.writeDataToServo(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, 2, destList[1])

                    runCount += 1