import math
import time
import Foundation.init as init
from Foundation.device import *
from Foundation.basis import *

from dynamixel_sdk import *
import dynamixel_sdk as dyn

class Lywal:

    # Robot basic parameters
    deltaT = 0.05
    clawState = [0, 0, 0, 0]
    wheelState = [0, 0, 0, 0]

    def __init__(self, id_list: list, portHandler, packetHandler):
        self.id_list = id_list
        self.portHandler = portHandler
        self.packetHandler = packetHandler
        for id in id_list:
            self.packetHandler.write2ByteTxRx(self.portHandler, id, ADDR_MX_CW, DXL_MULTI_MODE_CW_VALUE)
            self.packetHandler.write2ByteTxRx(self.portHandler, id, ADDR_MX_CCW, DXL_MULTI_MODE_CCW_VALUE)
            self.packetHandler.write2ByteTxRx(self.portHandler,id, ADDR_MX_OFFSET, 6000)

    def switchTorque(self, switch: str, *servoArray: list):
        targetServos = self.id_list
        if len(servoArray) != 0:
            targetServos = servoArray[0]
        if switch == 'enable':
            for id in targetServos:
                dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler,  1,ADDR_MX_MOVING_SPEED, 1124)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
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
                    # self.switchTorque('quit')
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                    # self.switchTorque('quit')
            if switch == 'quit':
                self.portHandler.closePort()
                quit(1)
        else:
            print("Insufficient parameters of switchTorque! ")
            self.switchTorque('quit')
        return

    def setSpeed(self, speedPercentage):
        deltaTRange = DELTA_T_MAX - DELTA_T_MIN
        self.deltaT = clamp(DELTA_T_MAX - (deltaTRange * speedPercentage / 100), DELTA_T_MIN, DELTA_T_MAX)

    # Option keys availiable: 
    # targetServo=targetServos: list, targetDict=toggle: bool, degree=toggle: bool
    def readPersentPosition(self, **options):
        dxl = []
        targetArray = self.id_list
        if 'targetServo' in options > 0:
            targetArray = options['targetServo']
        for id in targetArray:
            dxl1_present_position, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(
                self.portHandler, id, ADDR_MX_PRESENT_POSITION
            )
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                self.switchTorque('quit')
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                self.switchTorque('quit')
            if 'degree' in options and options['degree'] == True:
                dxl.append(positionalCodeToDeg(dxl1_present_position))
            else:
                dxl.append(dxl1_present_position)
        if 'targetDict' in options and options['targetDict'] == True:
            dxlDict = {}
            for index, value in enumerate(dxl):
                dxlDict[index + 1] = value
            return dxlDict

        return dxl
    
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

    def rotateServo(self, anglePairs: dict):
        targetDict = {}
        initialState: list = self.readPersentPosition()

        for index, (key, value) in enumerate(anglePairs.items()):
            targetDict[int(key)] = fancyRotate(initialState[key-1], degToPositionalCode(int(value)))
        self.writeData(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, targetDict)

    # Angle input in degrees. 
    def rotateGroup(self, angle: int, *servoList):
        targetArray = self.id_list
        if len(servoList) != 0:
            targetArray = servoList[0]
        angleSet, directionFlag = angle, 1
        if angle < 0:
            angleSet = -angle
            directionFlag = -1

        initialState = self.readPersentPosition()
        targetDict = {}

        runDegree = 0
        startTime = time.time()
        for group in getGroup(targetArray):
            self.wheelState[group - 1] += angle

        while runDegree < angleSet:
            if time.time() - startTime > runDegree * self.deltaT:
                for servo in targetArray:
                    if servo in [1, 3, 7, 8]:
                        targetDict[servo] = int(initialState[servo - 1] - (directionFlag * degToPositionalCode(runDegree)))
                    else:
                        targetDict[servo] = int(initialState[servo - 1] + (directionFlag * degToPositionalCode(runDegree)))
                runDegree += 1
                self.writeData(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, targetDict)

        time.sleep(1)

    def manipulateClaw(self, angle: int, servoList):
        if len(servoList) % 2 != 0:
            print('Manipulate claw for even amount of servos at a time, we\'re not continuing... ')
            self.switchTorque('quit')

        for clawIndex in getGroup(servoList):
            self.clawState[clawIndex - 1] += angle

        initialState = self.readPersentPosition()
        targetDict = {}
        angleSet, directionFlag = angle, 1
        if angle < 0:
            angleSet = -angle
            directionFlag = -1

        runDegree = 0
        startTime = time.time()
        while runDegree < angleSet:
            if time.time() - startTime > runDegree * self.deltaT:
                for servo in servoList:
                    targetDict[servo] = int(initialState[servo - 1] + (directionFlag * degToPositionalCode(runDegree)))
                self.writeData(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, targetDict)
                runDegree += 1

        time.sleep(1)

    def fourWheelDrive(self, rotation: int, directionArray: list):
        angleSet = rotation * 360
        directionFlagArray: list = [1, 1, 1, 1, 1, 1, 1, 1]
        for index, direction in enumerate(directionArray):
            directionFlagArray[servoMap[index * 2 + 1] - 1] = direction
            directionFlagArray[servoMap[index * 2 + 2] - 1] = direction
            self.wheelState[index] += direction * rotation * 360

        runDegree = 0
        startTime = time.time()
        initialState = self.readPersentPosition()
        targetDict = {}

        while runDegree < angleSet:
            if time.time() - startTime > runDegree * self.deltaT:
                for servo in self.id_list:
                    if servo in [1, 3, 7, 8]:
                        targetDict[servo] = int(initialState[servo - 1] - (directionFlagArray[servo - 1] * degToPositionalCode(runDegree)))
                    else:
                        targetDict[servo] = int(initialState[servo - 1] + (directionFlagArray[servo - 1] * degToPositionalCode(runDegree)))
                runDegree += 1
                self.writeData(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, targetDict)

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

        initialState = self.readPersentPosition(degree= True, targetDict=True)
        print('ii', initialState)
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
                    self.writeData(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, targetDict)

                    runCount += 1



        aftermath: dict = self.readPersentPosition(degree= True, targetDict=True)
        for index, (servoID, angle) in enumerate(aftermath.items()):
            aftermath[servoID] = initialState[servoID] - angle

        time.sleep(0.2)
        self.writeData(ADDR_MX_GOAL_POSITION, LEN_MX_GOAL_POSITION, initialState)

    def clawGrab(self):
        clawServos = [1, 2, 3, 4]
        
        # 向前滚
        self.rotateGroup(120)
        time.sleep(1)
        
        # 前轮张开一定角度
        self.manipulateClaw(30, clawServos)
        time.sleep(1)
        
        # 向前滚一定角度
        self.rotateGroup(60)
        time.sleep(1)
        
        # 前轮夹起棍子
        self.manipulateClaw(-20, clawServos)
        time.sleep(1)
        
        # 向后转
        self.rotateGroup(-240)
        time.sleep(1)

    # TODO: Much debugging. 
    def rotatePositionZero(self, *servoGroups: list):
        targetServoGroups = [1, 2, 3, 4]
        if len(servoGroups) != 0:
            targetServoGroups = servoGroups

        for clawIndex, clawValue in enumerate(self.clawState):
            if clawValue == 0 or (clawIndex + 1 not in targetServoGroups):
                continue
            print('Claw', clawIndex + 1, 'to reset. ')
            print('Value', -clawValue)
            self.manipulateClaw(-clawValue, readGroup([clawIndex + 1]))
            print('After that, the claw state is', self.clawState)

        time.sleep(1)

        for wheelIndex, wheelValue in enumerate(self.wheelState):
            if wheelValue % 360 == 0 or (wheelIndex + 1 not in targetServoGroups):
                continue
            print('Wheel', wheelIndex, 'to reset. ')
            print('Value', -optimalResetRotation(wheelValue))
            self.rotateGroup(-optimalResetRotation(wheelValue), readGroup([wheelIndex + 1]))
            print('After that, the wheel state is', self.wheelState)

        time.sleep(1)
