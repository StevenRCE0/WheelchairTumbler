import sys

# Check which port is being used on your controller
def device():
    if 'darwin' in sys.platform:
        return '/dev/tty.usbserial-A105IP0D'
    elif 'nt' in sys.platform:
        return 'COM5'
    else:
        return '/dev/ttyUSB0'

def openPort(definedPortHandler):
    try:
        definedPortHandler.openPort()
    except:
        print("Failed to open the port")
        print("Press any key to terminate...")
        getch()
        quit()
    else:
        print("Succeeded to open the port")
        
def closePort(definedPortHandler):
    definedPortHandler.closePort()

def setBaudRate(definedPortHandler, targetBaudRate):
    try:
        definedPortHandler.setBaudRate(targetBaudRate)
    except:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        getch()
        quit()
    else:
        print("Succeeded to change the baudrate")

class getch():
    def __init__(self):
        try:
            self.impl = self._GetchWindows()
        except:
            self.impl = self._GetchUnix()

    def __str__(self):
        return self.impl

    def _GetchUnix(self):
        import readchar
        return readchar.readchar()

    def _GetchWindows(self):
        import msvcrt
        return msvcrt.getch()