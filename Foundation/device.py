import sys

# Check which port is being used on your controller
def device():
    if 'darwin' in sys.platform:
        return '/dev/tty.usbserial-*'
    elif 'nt' in sys.platform:
        return 'COM5'
    else:
        return '/dev/ttyUSB0'

def openPort(definedPortHandler):
    try:
        definedPortHandler.openPort()                                                    #开启端口
    except:
        print("Failed to open the port")
        print("Press any key to terminate...")
        getch()
        quit()
    else:
        print("Succeeded to open the port")

class getch():
    def __init__(self):
        try:
            self.impl = self._GetchWindows()
        except:
            self.impl = self._GetchUnix()

    def __str__(self):
        return self.impl

    def _GetchUnix(self):
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def _GetchWindows(self):
        import msvcrt
        return msvcrt.getch()