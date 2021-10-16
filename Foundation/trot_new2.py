import math
def trot_new2(time) :
#void walktra(doubletime, int,leg_ID)
    T=2
    stepT=T
    steptime =time%stepT
    stepH=15
    stepV=3#每步距离
    steph=4
    C=1
    if steptime<stepT/2 :
# xset=-stepV*stepT/4*0.55+steptime*stepV;
        xset=C+stepV*(math.sin(steptime*math.pi/stepT))**3
        yset=stepH-steph*(math.sin(2*steptime*math.pi/stepT))**3
    else:
#  xset=C+stepV*stepT/4-(steptime-stepT/4)*stepV/3;
        xset=C+stepV-stepV*(math.sin((steptime-stepT/2)*math.pi/stepT))**3
        yset=stepH
    xh=xset
    yh=yset
    return [xh,yh]