import sys

def device():
    if 'darwin' in sys.platform:
        return '/dev/tty.usbserial-*'
    elif 'nt' in sys.platform:
        return 'COM5'
    else:
        return '/dev/ttyUSB0'

# Check which port is being used on your controller

class Getch():
    def __init__(self):
        try:
            self.impl = self._GetchWindows()
        except:
            self.impl = self.GetchUnix()

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