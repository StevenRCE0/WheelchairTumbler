import Foundation.device as device

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

def clamp(input, min, max):
    if input > max: return max
    if input < min: return min
    return input