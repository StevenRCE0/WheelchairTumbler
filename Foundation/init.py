from Foundation.nijie import nijie
from Foundation.trotTrail import trotTrail
# import matplotlib.pyplot as plt

def init(T, detT):

    def emptyDesthArrays() -> tuple:
        return ([], [], [], [], [], [], [], [])

    Desth1, Desth2, Desth3, Desth4, Desth5, Desth6, Desth7, Desth8 = emptyDesthArrays()
    paramDict = {
        'T': 2,
        'stepH': 15,
        'stepV': 3,     # Step span
        'steph': 4,
        'C': 1
    }
    
    [x1, y1] = trotTrail(0    , paramDict, 4)            # 电机12左前腿
    [x2, y2] = trotTrail(T / 2, paramDict, 4)            # 电机34右前腿
    [x3, y3] = trotTrail(T / 2, paramDict, 3)            # 电机68右后腿
    [x4, y4] = trotTrail(0    , paramDict, 2)            # 电机57左后腿

    desth1, desth2 = nijie(x1, y1)
    desth3, desth4 = nijie(x2, y2)
    desth6, desth8 = nijie(x3, y3)
    desth7, desth5 = nijie(x4, y4)

    Desth1.append(desth1);Desth2.append(desth2);Desth3.append(desth3);Desth4.append(desth4)
    Desth5.append(desth5);Desth6.append(desth6);Desth7.append(desth7);Desth8.append(desth8)

    for dest in range(int(detT * 100),int(T * 100),int(detT * 100)):
        dest = dest/100
        [x1, y1] = trotTrail(dest, paramDict, 4)
        [x2, y2] = trotTrail(dest + T / 2, paramDict, 4)
        [theta1_a, theta2_a] =  nijie(x1, y1)
        [theta3_a, theta4_a] =  nijie(x2, y2)

        Desth1.append(theta1_a)
        Desth2.append(theta2_a)
        Desth3.append(theta3_a)
        Desth4.append(theta4_a)

    for dest in range(int(T * 100 - detT * 100), 0, int(-detT * 100)):
        dest = dest / 100
        [x3, y3] = trotTrail(dest+T/2, paramDict, 3)
        [x4, y4] = trotTrail(dest, paramDict, 2)
        [theta6_a, theta8_a] = nijie(x3, y3)
        [theta7_a, theta5_a] = nijie(x4, y4)
        
        Desth5.append(theta5_a)
        Desth6.append(theta6_a)
        Desth7.append(theta7_a)
        Desth8.append(theta8_a)

    return [Desth1, Desth2, Desth3, Desth4, Desth5, Desth6, Desth7, Desth8]
