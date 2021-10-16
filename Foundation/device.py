import sys

def device():
    if 'darwin' in sys.platform:
        return '/dev/tty.usbserial-*'
    elif 'nt' in sys.platform:
        return 'COM5'
    else:
        return '/dev/ttyUSB0'

# Check which port is being used on your controller