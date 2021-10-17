import Foundation.nijie as nijie
import Foundation.trot_new2 as trot_new2
import Foundation.trot_new3 as trot_new3
import Foundation.trot_new4 as trot_new4
import matplotlib.pyplot as plt

def init(T,detT):
    Desth1=[]
    Desth2= [];Desth3=[];Desth4=[];Desth5=[];Desth6=[];Desth7=[];Desth8=[]
    [x1, y1] = trot_new4.trot_new4(0)                      # 电机12左前腿
    [x2, y2] = trot_new4.trot_new4(T / 2)                   #电机3，4右前腿
    [x3, y3] =trot_new3.trot_new3(T / 2)                        # 电机6，8右后腿
    [x4, y4] = trot_new2.trot_new2(0)                 # 电机5，7左后腿
    desth1, desth2 = nijie.nijie(x1, y1)
    desth3, desth4= nijie.nijie(x2, y2)
    desth6, desth8 = nijie.nijie(x3, y3)
    desth7, desth5= nijie.nijie(x4, y4)
    Desth1.append(desth1);Desth2.append(desth2);Desth3.append(desth3);Desth4.append(desth4)
    Desth5.append(desth5);Desth6.append(desth6);Desth7.append(desth7),Desth8.append(desth8)
    for dest in range(int(detT*100),int(T*100),int(detT*100)):
        dest=dest/100
        [x1, y1] = trot_new4.trot_new4(dest)
        [x2, y2] = trot_new4.trot_new4(dest + T / 2)
        [theta1_a, theta2_a] =  nijie.nijie(x1, y1)
        [theta3_a, theta4_a] =  nijie.nijie(x2, y2)

        Desth1.append(theta1_a)
        Desth2.append(theta2_a)
        Desth3.append(theta3_a)
        Desth4.append(theta4_a)
    for dest in range(int(T * 100 - detT * 100), 0, int(-detT * 100)):
        dest = dest / 100
        [x3, y3] = trot_new3.trot_new3(dest+T/2)
        [x4, y4] = trot_new2.trot_new2(dest)
        [theta6_a, theta8_a] = nijie.nijie(x3, y3)
        [theta7_a, theta5_a] = nijie.nijie(x4, y4)
        Desth5.append(theta5_a)
        Desth6.append(theta6_a)
        Desth7.append(theta7_a)
        Desth8.append(theta8_a)

    return[Desth1,Desth2,Desth3,Desth4,Desth5,Desth6,Desth7,Desth8]
