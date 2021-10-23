import math
import time
import Foundation.init as init
from Foundation.device import *
from Foundation.basis import *

from dynamixel_sdk import *

class Lywal:

    # Robot basic parameters
    mode = 'wheel_mode'
    jointSpeed = 100
    deltaT = 0.05
    initialPositions = []
    positionZero = []

    def __init__(self, id_list: list, portHandler, packetHandler):
        self.id_list = id_list
        self.portHandler = portHandler
        self.packetHandler = packetHandler
        self.initialPositions: list = self.readPersentPosition()

    def switchTorque(self, switch: str, *servoArray: list):
        targetServos = self.id_list
        if len(servoArray) != 0:
            targetServos = servoArray[0]
        if switch == 'enable':
            for id in targetServos:
                dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, id, ADDR_MX_TORQUE_ENABLE, 1)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        elif switch == 'disable' or 'quit':
            for id in targetServos:
                dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, id, ADDR_MX_TORQUE_ENABLE,
                                                                        TORQUE_DISABLE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            if switch == 'quit':
                quit(1)
        else:
            print("Insufficient parameters of switch_torque! ")
            self.switchTorque('quit')
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
            servoArray = servoParam[0]
    
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
        dxl = []
        targetArray = self.id_list
        if len(targetServo) > 0:
            targetArray = targetServo
        for id in targetArray:
            dxl1_present_position, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(
                self.portHandler, id, ADDR_MX_PRESENT_POSITION
            )
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
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
                self.switchTorque('quit')
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
                self.switchTorque('quit')

        dxl_comm_result = groupSyncWrite.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))

        groupSyncWrite.clearParam()

    def rotateJoints(self, anglePairs: dict):
        targetDict = {}
        initialState: list = self.readPersentPosition()

        if self.mode != 'multi_mode':
            print('Lywal was not set to multi mode, continuing in multi mode... ')
            self.switchMode('multi_mode')

        for index, (key, value) in enumerate(anglePairs.items()):
            targetDict[int(key)] = fancyRotate(initialState[key-1], degToPositionalCode(int(value)))
        self.writeData(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, targetDict)

    # Rotate in multi mode. Angle input in degrees. 
    def rotateGroup(self, angle: int, *servoList):
        targetArray = self.id_list
        if len(servoList) != 0:
            targetArray = servoList[0]
        angleSet, directionFlag = angle, 1
        if angle < 0:
            angleSet = -angle
            directionFlag = -1

        if self.mode != 'multi_mode':
            print('Lywal was not set to multi mode, continuing in multi mode... ')
            self.switchMode('multi_mode')

        runDegree = 0
        startTime = time.time()
        initialState = self.readPersentPosition()
        targetDict = {}

        while runDegree < angle:
            if time.time() - startTime > runDegree * self.deltaT:
                for servo in targetArray:
                    if servo in [0, 2, 6, 7]:
                        targetDict[servo] = int(initialState[servo] - (directionFlag * degToPositionalCode(runDegree)))
                    else:
                        targetDict[servo] = int(initialState[servo] + (directionFlag * degToPositionalCode(runDegree)))
                runDegree += 1
                self.writeData(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, targetDict)

    def manipulateClaw(self, angle: int, servoList):
        if len(servoList) != 4:
            print('Manipulate claw for 4 servos at a time, we\'re not continuing... ')
            self.switchTorque('quit')

        if self.mode != 'multi_mode':
            print('Lywal was not set to multi mode, continuing in multi mode... ')
            self.switchMode('multi_mode')

        runDegree = 0
        startTime = time.time()
        initialState = self.readPersentPosition()
        targetDict = {}

        while runDegree < angle:
            if time.time() - startTime > runDegree * self.deltaT:
                for servo in servoList:
                    targetDict[servo] = int(initialState[servo] + degToPositionalCode(runDegree))
                runDegree += 1
                self.writeData(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, targetDict)

    def rotateToZero(self):
        if len(self.positionZero) !=  8:
            print('Position zero has not been set. ')
            self.switchTorque('quit')
        targetDict = {}
        for index, value in enumerate(self.readPersentPosition()):
            offest = positionalCodeToDeg((self.positionZero[index] % 4096) - (value % 4096))
            if index == 5:
                offest = offest - 360
            targetDict[index + 1] = offest
        # targetDict = resolveRotationConflict(targetDict)
        print(targetDict)
        self.rotateJoints(targetDict)

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

    # Parameter dictionary includes "repetitive: int" and "servos: list". 
    def trot(self, **paramOptions: dict):
        repetitiveSet: int = 1
        if 'repetitive' in paramOptions and paramOptions['repetitive'] > 0:
            repetitiveSet = 1
        durationSet: int = 3
        if 'duration' in paramOptions and paramOptions['duration'] > 0:
            repetitiveSet = paramOptions['duration']
        targetServo: list = self.id_list
        if 'servos' in paramOptions and len(paramOptions['servos']) in range(1, 8):
            targetServo = paramOptions['servos']
        
        destList = []        

        for occurrence in range(repetitiveSet):
            runCount, desiredCount = 0, 500
            T, deltaT = 2.0, 0.2
            startTime  = time.time()
            desth = init.init(T, deltaT)
            dxl = self.readPersentPosition()

            while runCount < desiredCount and time.time() - startTime < durationSet:
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
                    for index, servo in enumerate(targetServo):
                        targetDict[servo] = destList[index]

                    print('Troting: ')
                    print(targetDict)
                    self.writeData(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, targetDict)

                    runCount += 1

    def claw(self):
        clawServos = [1, 2, 3, 4]
        
        # 向前滚
        self.rotateGroup(120)
        time.sleep(1)
        
        # 前轮张开一定角度
        self.manipulateClaw(15, clawServos)
        time.sleep(1)
        
        # 向前滚一定角度
        self.rotateGroup(60)
        time.sleep(1)
        
        # 前轮夹起棍子
        self.manipulateClaw(-6, clawServos)
        time.sleep(1)
        
        # 向后转
        self.rotateGroup(-240)
        time.sleep(1)
