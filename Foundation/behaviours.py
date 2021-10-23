import math
import numpy as np
import time
import Foundation.init as init
from Foundation.device import *
from Foundation.basis import *
from Foundation.nijie import nijie

from dynamixel_sdk import *

class Lywal:

    mode = 'wheel_mode'
    jointSpeed = 100
    initialPositions = []
    positionZero = []

    def __init__(self, id_list: list, portHandler, packetHandler):
        self.id_list = id_list
        self.portHandler = portHandler
        self.packetHandler = packetHandler
        self.initialPositions: list = self.readPersentPosition()

    def switchTorque(self, switch: str):
        if switch == 'enable':
            for id in self.id_list:
                dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, id, ADDR_MX_TORQUE_ENABLE, 1)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("Dynamixel#" + str(id) + " has been successfully connected")
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

# TODO: make this work
    def setSpeed(self, powerPairs: dict):
        if self.mode == 'wheel_mode':
            print('In wheel mode, there\'s no need for setSpeed function. ')
            return

        targetDict = {}
        for index, (key, value) in enumerate(powerPairs.items()):
            if value == 100:
                targetDict[key] = 0
                continue
            targetValue = int(clamp(409.6 * value, 1, 1023))
            targetDict[key] = targetValue
        print(targetDict)
        self.writeData(ADDR_MX_MOVING_SPEED, LEN_MX_MOVING_SPEED, targetDict)

    def switchMode(self, mode_name: str, *servoParam: list):
        servoArray = self.id_list
        if len(servoParam) != 0:
            servoArray = servoParam
    
        if mode_name == 'wheel_mode':
            for id in servoArray:
                self.packetHandler.write2ByteTxRx(self.portHandler, id, ADDR_MX_CW, DXL_WHEEL_MODE_CW_VALUE)
                self.packetHandler.write2ByteTxRx(self.portHandler,id, ADDR_MX_CCW, DXL_WHEEL_MODE_CCW_VALUE)
                self.packetHandler.write2ByteTxRx(self.portHandler, id, ADDR_MX_OFFSET, 6000)
        elif mode_name == 'multi_mode':
            for id in servoArray:
                self.packetHandler.write2ByteTxRx(self.portHandler, id, ADDR_MX_CW, DXL_MULTI_MODE_CW_VALUE)
                self.packetHandler.write2ByteTxRx(self.portHandler, id, ADDR_MX_CCW, DXL_MULTI_MODE_CCW_VALUE)
                self.packetHandler.write2ByteTxRx(self.portHandler,id, ADDR_MX_OFFSET, 6000)
        elif mode_name == 'joint_mode':
            for id in servoArray:
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

    def writeDataAll(self, adr, adr_len, data):
        groupSyncWrite = GroupSyncWrite(self.portHandler, self.packetHandler, adr, adr_len)
        param_goal_positions = []

        for i in range(len(self.id_list)):
            param_goal_positions.append([
                DXL_LOBYTE(DXL_LOWORD(data[i])),DXL_HIBYTE(DXL_LOWORD(data[i])),
                DXL_LOBYTE(DXL_HIWORD(data[i])),DXL_HIBYTE(DXL_HIWORD(data[i]))
            ])

        for i in range(len(self.id_list)):
            dxl_addparam_result = groupSyncWrite.addParam(self.id_list[i],param_goal_positions[i])
            if dxl_addparam_result != True:
                print("[ID:%03d] groupSyncWrite addparam failed" % self.id_list[i])
                quit()
        dxl_comm_result = groupSyncWrite.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))

        groupSyncWrite.clearParam()
    
    def writeData(self, adr, adr_len, dataPairs: dict):
        groupSyncWrite = GroupSyncWrite(self.portHandler, self.packetHandler, adr, adr_len)
        for index, (key, value) in enumerate(dataPairs.items()):
            target = [
                DXL_LOBYTE(DXL_LOWORD(value)), DXL_HIBYTE(DXL_LOWORD(value)),
                DXL_LOBYTE(DXL_HIWORD(value)), DXL_HIBYTE(DXL_HIWORD(value))
            ]
            dxl_addparam_result = groupSyncWrite.addParam(key, target)
            if dxl_addparam_result != True:
                print(dxl_addparam_result)
                print("[Index:" + str(index) + ", ID:" + str(key) + "] groupSyncWrite addparam failed")
                self.switchTorque('disable')
                quit()

        dxl_comm_result = groupSyncWrite.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))

        groupSyncWrite.clearParam()

    def rotateJoints(self, anglePairs: dict):
        targetDict = {}
        initialState: list = self.readPersentPosition()
        print("\n")
        print(initialState)
        print("\n")
        for index, (key, value) in enumerate(anglePairs.items()):
            targetDict[int(key)] = fancyRotate(initialState[key-1], degToPositionalCode(int(value)))
            print("target: " + str(degToPositionalCode(int(value))))
            print("current: " + str(initialState[key-1]))
            print("fancy: " + str(fancyRotate(initialState[key-1], degToPositionalCode(int(value)))))
        self.writeData(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, targetDict)

# TODO: not tested yet
    def rotateToZero(self):
        if len(self.positionZero) !=  8:
            print('Position zero has not been set. ')
            self.switchTorque('disable')
            quit(1)
        targetDict = {}
        for index, value in enumerate(self.readPersentPosition()):
            offest = value // 4096 - self.positionZero[index] // 4096
            targetDict[index + 1] = offest
        self.writeData(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, targetDict)

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
            -powerArray[2], -powerArray[3]
        ]

        for groupIndex, power in enumerate(rectifiedPowerArray):
            if power == 0:
                continue
            self.packetHandler.write2ByteTxRx(self.portHandler, servoMap[groupIndex * 2 + 1], ADDR_MX_MOVING_SPEED, constructPower(power, 0))
            self.packetHandler.write2ByteTxRx(self.portHandler, servoMap[groupIndex * 2 + 2], ADDR_MX_MOVING_SPEED, constructPower(power, 1))

# Parameter dictionary contains "repetitive: int" and "servos: list". 
    def trot(self, **paramOptions: dict):
        repetitiveSet: int = 0
        if 'repetitive' not in paramOptions or paramOptions-'repetitive' <= 0:
            repetitiveSet = 1
        else:
            repetitiveSet = paramOptions['repetitive']
        
        targetServos: list = self.id_list
        if 'servos' in paramOptions and len(paramOptions['servos']) in range(1, 8):
            targetServos = paramOptions['servos']
        
        destList = []        

        for occurrence in range(repetitiveSet):
            runCount, desiredCount = 0, 500
            T, deltaT = 2.0, 0.2
            startTime  = time.time()
            desth = init.init(T, deltaT)
            dxl = self.readPersentPosition()

            while runCount < desiredCount and time.time() - startTime < 10:
                currentStartTime = time.time() - startTime
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

                    targetDict = {}
                    for index, servo in enumerate(targetServos):
                        targetDict[servo] = destList[index]
                    self.writeData(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, targetDict)
                    #  self.writeDataAll(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, destList)

                    runCount += 1

    def claw(self):
        Theta= [i for i in range(1, 9)]
        id = [1,2,3,4]
        Theta1 = [1,2,3,4]
        detT, x = 0.05, 0

        t0 = time.time()                             #向前滚
        dxl = self.readPersentPosition()

        while x < 121:
            t = time.time() - t0
            if t > x * detT:
                for i in [0,2,6,7]:
                    Theta[i] = int(dxl[i] - 4096 / 360 *1*x)
                for i in [1,3,4,5]:
                    Theta[i] = int(dxl[i] + 4096 / 360 *1*x)
                x = x + 1
                self.writeDataAll(self.id_list, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta)
        time.sleep(1)                         #前轮张开一定角度
        # id = [1,2]
        dxl = self.readPersentPosition()
        # Theta1 = [1,2]
        for i in enumerate(Theta1.items()):
            Theta1[i] = int(4096 / 360 * 15+ dxl[i])

        self.writeDataAll(id, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta1)
        time.sleep(1)                            #向前滚一定角度
        t0 = time.time()
        x = 0
        dxl = self.readPersentPosition()
        while x<60:
            t = time.time() - t0
            if t> x *detT:
                for i in [0,2,6,7]:#[0,2,6,7]:
                    Theta[i] = int(dxl[i] -4096 / 360 *1*x)
                for i in [1,3,4,5]:#[1,3,4,5]:
                    Theta[i] = int(dxl[i] +4096 / 360 *1*x)
                x = x + 1
                self.writeDataAll(self.id_list, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta)
        dxl = self.readPersentPosition(id)
        time.sleep(1)                                   #前轮夹起棍子
        dxl = self.readPersentPosition(id)
        for i in range(len(Theta1)):
            Theta1[i] = int(-4096 / 360 * 6+ dxl[i])
        self.writeDataAll(id, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta1)
        x=0
        time.sleep(1)                                   #向后转
        dxl = self.readPersentPosition()
        t0 = time.time()
        while x<240:
            t = time.time() - t0
            if t> x *detT:
                for i in [0,2,6,7]:#[0,2,6,7]:
                    Theta[i] = int(dxl[i] +4096 / 360 *1* x)
                for i in [1,3,4,5]:#[1,3,4,5]:
                    Theta[i] = int(dxl[i] -4096 / 360 *1* x)
                x = x + 1
                self.writeDataAll(self.id_list, ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, Theta)
