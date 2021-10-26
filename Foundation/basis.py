import Foundation.device as device

# Control table address
ADDR_MX_CW                  = 6
ADDR_MX_CCW                 = 8
ADDR_MX_OFFSET              = 20
ADDR_MX_TORQUE_ENABLE       = 24         #Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION       = 30
ADDR_MX_MOVING_SPEED        = 32
ADDR_MX_PRESENT_POSITION    = 36
ADDR_MX_PRESENT_LOAD        = 40

LEN_MX_GOAL_POSITION        = 4
LEN_MX_PRESENT_LOAD         = 4

DEVICENAME                  = device.device()

# Protocol version
PROTOCOL_VERSION            = 1.0       # See which protocol version is used in the Dynamixel
BAUDRATE                    = 115200    # Dynamixel default baudrate : 57600
TORQUE_ENABLE               = 1         # Value for enabling the torque
TORQUE_DISABLE              = 0         # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 100       # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 900       # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 10        # Dynamixel moving status threshold

# Mode presets
DXL_MULTI_MODE_CW_VALUE     = 4095
DXL_WHEEL_MODE_CW_VALUE     = 0
DXL_MULTI_MODE_CCW_VALUE    = 4095
DXL_WHEEL_MODE_CCW_VALUE    = 0
DXL_JOINT_MODE_CW_VALUE     = 0
DXL_JOINT_MODE_CCW_VALUE    = 4095
VELOCITY_MODE               = 1
POSITION_MODE               = 3
# dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]  # Goal position

DELTA_T_MIN                 = 0
DELTA_T_MAX                 = 0.1
servoMap = {1:1, 2:2, 3:3, 4:4, 5:5, 6:7, 7:6, 8:8}

def initializeRotationDict() -> dict:
    result = {}
    for index in range(1, 9):
        result[index] = -85
    return result

def clamp(input, min, max):
    if input > max: return max
    if input < min: return min
    return input

def degToPositionalCode(degree, *clampRange) -> int:
    ratio = 4096 / 360
    if len(clampRange) == 2:
        return int(clamp(ratio * degree, clampRange[0], clampRange[1]))
    else:
        return int(ratio * degree)

def positionalCodeToDeg(positionalCode) -> int:
    ratio = 360 / 4096
    return int(ratio * positionalCode)

# Angles provided in positional codes. 
def fancyRotate(current: int, target: int) -> int:
    return current + target

def optimalResetRotation(angle: int) -> int:
    if angle % 360 <= 180:
        return angle % 360
    else:
        return 360 - (angle % 360)

def getGroup(servoArray: list) -> list:
    result = []
    if [1, 2] in servoArray:
        result.append(1)
    if [3, 4] in servoArray:
        result.append(2)
    if [5, 7] in servoArray:
        result.append(3)
    if [6, 8] in servoArray:
        result.append(4)
    return result

def readGroup(groupArray: list) -> list:
    result = []
    if 1 in groupArray:
        result.append(1, 2)
    if 2 in groupArray:
        result.append(3, 4)
    if 3 in groupArray:
        result.append(5, 7)
    if 4 in groupArray:
        result.append(6, 8)
    return result