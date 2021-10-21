import math
import numpy as np
from time import time, sleep
import Foundation.init as init
from Foundation.device import *
from Foundation.basis import *
from Foundation.nijie import nijie

from dynamixel_sdk import *

class Lywal:

    mode = 'wheel_mode'

    def __init__(self, id_list: list, portHandler, packetHandler):
        self.id_list = id_list
        self.portHandler = portHandler
        self.packetHandler = packetHandler

    def switchTorque(self, switch: str):
        if switch == 'enable':
            for id in self.id_list:
                dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, id, ADDR_MX_TORQUE_ENABLE, 1)
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

    def switchMode(self, mode_name: str):
        if mode_name == 'wheel_mode':
            for id in self.id_list:
                self.packetHandler.write2ByteTxRx(self.portHandler, id, ADDR_MX_CW, DXL_WHEEL_MODE_CW_VALUE)
                self.packetHandler.write2ByteTxRx(self.portHandler,id, ADDR_MX_CCW, DXL_WHEEL_MODE_CCW_VALUE)
                self.packetHandler.write2ByteTxRx(self.portHandler, id, ADDR_MX_OFFSET, 6000)
        elif mode_name == 'multi_mode':
            for id in self.id_list:
                self.packetHandler.write2ByteTxRx(self.portHandler, id, ADDR_MX_CW, DXL_MULTI_MODE_CW_VALUE)
                self.packetHandler.write2ByteTxRx(self.portHandler, id, ADDR_MX_CCW, DXL_MULTI_MODE_CCW_VALUE)
                self.packetHandler.write2ByteTxRx(self.portHandler,id, ADDR_MX_OFFSET, 6000)
        elif mode_name == 'joint_mode':
            for id in self.id_list:
                self.packetHandler.write2ByteTxRx(self.portHandler, id, ADDR_MX_CW, DXL_JOINT_MODE_CW_VALUE)
                self.packetHandler.write2ByteTxRx(self.portHandler, id, ADDR_MX_CCW, DXL_JOINT_MODE_CCW_VALUE)
                self.packetHandler.write2ByteTxRx(self.portHandler,id, ADDR_MX_OFFSET, 6000)
        else:
            return

        self.mode = mode_name

    def readPersentPosition(self, *targetServo: list) -> list:
        dxl=[]
        targetArray = self.id_list
        if len(targetServo) > 0:
            targetArray = targetServo
        for id in targetArray:
            # Read Dynamixel present position
            dxl1_present_position, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(
                self.portHandler, id, ADDR_MX_PRESENT_POSITION
            )
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
    
    def writeDataToServo(self, adr, adr_len, servoID: int, position: int):
        groupSyncWrite = GroupSyncWrite(self.portHandler, self.packetHandler, adr, adr_len)
        param_goal_position = [
            DXL_LOBYTE(DXL_LOWORD(position)),
            DXL_HIBYTE(DXL_LOWORD(position)),
            DXL_LOBYTE(DXL_HIWORD(position)),
            DXL_HIBYTE(DXL_HIWORD(position))
        ]
        dxl_addparam_result = groupSyncWrite.addParam(servoID, param_goal_position)
        if dxl_addparam_result != True:
            print("[ID:%03d] groupSyncWrite addparam failed" % servoID)
            quit()
        dxl_comm_result = groupSyncWrite.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))

        groupSyncWrite.clearParam()
        
    def rotateJoints(self, anglePairs: dict):
        currentPositions = self.readPersentPosition()
        for index, (key, value) in enumerate(anglePairs.items()):
            self.writeDataToServo(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, int(key), fancyRotate(currentPositions[index], degToPositionalCode(int(value)), directionMap[key]))
            print("target: " + str(degToPositionalCode(int(value))))
            print("current: " + str(currentPositions[index]))
            print("fancy: " + str(fancyRotate(currentPositions[index], degToPositionalCode(int(value)), directionMap[key])))
            

    def drive(self, powerArray: list):
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
            print("Expecting 4 groups of servo. ")
            return

        rectifiedPowerArray = [
            powerArray[0], powerArray[1],
            -powerArray[3], -powerArray[4]
        ]

        for groupIndex in range(0, len(powerArray)):
            self.packetHandler.write2ByteTxRx(self.portHandler, servoMap[groupIndex * 2 + 1], ADDR_MX_MOVING_SPEED, constructPower(powerArray[groupIndex], 0))
            self.packetHandler.write2ByteTxRx(self.portHandler, servoMap[groupIndex * 2 + 2], ADDR_MX_MOVING_SPEED, constructPower(powerArray[groupIndex], 1))

    def trot(self, *repetitive: int):
        repetitiveSet: int = 0
        if len(repetitive) == 0 or repetitive[0] <= 0:
            repetitiveSet = 1
        else:
            repetitiveSet = repetitive[0]
        destList = []

        for occurrence in range(repetitiveSet):
            runCount, desiredCount = 0, 500
            T, deltaT = 2.0, 0.2
            startTime  = time()
            desth = init.init(T, deltaT)
            dxl = self.readPersentPosition()

            while runCount < desiredCount and time() - startTime < 10:
                currentStartTime = time() - startTime
                if currentStartTime > runCount * deltaT:
                    destIndex = int(math.floor((runCount) % (T / deltaT)))
                    if destIndex == 40:
                        destIndex = 0
                    
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

                    self.writeData(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, destList)
                    runCount += 1

    def claw(self):
        Theta= [i for i in range(1, 9)]
        id = [1,2,3,4]
        Theta1 = [1,2,3,4]
        detT, x = 0.05, 0

        t0 = time()                             #向前滚
        dxl = self.readPersentPosition()

        while x < 121:
            t = time() - t0
            if t > x * detT:
                for i in [0,2,6,7]:
                    Theta[i] = int(dxl[i] - 4096 / 360 *1*x)
                for i in [1,3,4,5]:
                    Theta[i] = int(dxl[i] + 4096 / 360 *1*x)
                x = x + 1
                self.writeData(self.id_list, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta)
        time.sleep(1)                         #前轮张开一定角度
        # id = [1,2]
        dxl = self.readPersentPosition()
        # Theta1 = [1,2]
        for i in enumerate(Theta1.items())
            Theta1[i] = int(4096 / 360 * 15+ dxl[i])

        self.writeData(id, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta1)
        time.sleep(1)                            #向前滚一定角度
        t0 = time()
        x = 0
        dxl = self.readPersentPosition()
        while x<60:
            t = time() - t0
            if t> x *detT:
                for i in [0,2,6,7]:#[0,2,6,7]:
                    Theta[i] = int(dxl[i] -4096 / 360 *1*x)
                for i in [1,3,4,5]:#[1,3,4,5]:
                    Theta[i] = int(dxl[i] +4096 / 360 *1*x)
                x = x + 1
                self.writeData(self.id_list, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta)
        dxl = self.readPersentPosition(id)
        time.sleep(1)                                   #前轮夹起棍子
        dxl = self.readPersentPosition(id)
        for i in range(len(Theta1)):
            Theta1[i] = int(-4096 / 360 * 6+ dxl[i])
        write_data(id, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta1)
        x=0
        time.sleep(1)                                   #向后转
        dxl = readpersentposition(id_list)
        t0 = time()
        while x<240:
            t = time() - t0
            if t> x *detT:
                for i in [0,2,6,7]:#[0,2,6,7]:
                    Theta[i] = int(dxl[i] +4096 / 360 *1* x)
                for i in [1,3,4,5]:#[1,3,4,5]:
                    Theta[i] = int(dxl[i] -4096 / 360 *1* x)
                x = x + 1
                write_data(id_list, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta)
