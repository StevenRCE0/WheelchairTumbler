"""

    Calculate the trail for the legs as the positive reslution. 
    This module combines the 2~4 trot_new definitions. 

"""

from math import pi, sin

def trotTrail(time: int, paramDict: dict, mode: int) -> list:
    stepT = paramDict['T']
    stepTime =time % stepT

    if stepTime < stepT / 2:
# xset=-stepV*stepT/4*0.55+steptime*stepV;
        xSet = paramDict['C'] + paramDict['stepV'] * (sin(stepTime * pi / stepT)) ** 3
        ySet = paramDict['stepH'] - paramDict['steph'] * (sin(2 * stepTime * pi / stepT)) ** 3
    else:
# xset=C+stepV*stepT/4-(steptime-stepT/4)*stepV/3;
        xSet = paramDict['C'] + paramDict['stepV'] - paramDict['stepV'] * (sin((stepTime - stepT / 2) * pi / stepT)) ** 3
        ySet = paramDict['stepH']

    if mode == 2:
        xSet = xSet
        ySet = ySet
    elif mode == 3:
        xSet = -xSet
        ySet = ySet
    elif mode == 4:
        xSet = -xSet
        ySet = ySet

    return [xSet, ySet]