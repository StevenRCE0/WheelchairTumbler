import math
def zhengjie(ang1,ang2):
    theta2=ang2*0.0175
    theta1=ang1*0.0175
    a=9                               #半径
    b=9*(3**0.5)
    y1=a*math.cos((theta2-theta1)*0.5)
    y2 = b *math.sqrt(1 -( (a * (math.cos(theta1) - math.cos(theta2)))**2+ (a * (math.sin(theta1) - math.sin(theta2)))**2)/ 972.0)
    AA = y1 + y2
    x = AA * math.cos((theta1 + theta2) / 2)
    y = AA * math.sin((theta1 + theta2) / 2)
    r=9
    ax=math.cos(theta1)*9
    ay=math.sin(theta1)*9
    theta11=math.atan((y-ay)/(ax-x))
    mx1 = (ax + x) / 2
    my1 = (ay + y) / 2
    ox1 = -(r / 2) * math.cos(1.57079 - theta11) + mx1
    oy1 = -(r / 2) * math.sin(1.57079 - theta11) + my1

    cx = math.cos(theta2) * 9
    cy = math.sin(theta2) * 9
    theta22 = math.atan((y - cy) / (x - cx))
    mx2 = (cx + x) / 2
    my2 = (cy + y) / 2
    ox2 = (r / 2) *math. cos(1.57079 - theta22) + mx2
    oy2 = -(r / 2) * math.sin(1.57079 - theta22) + my2
    yyy = 9 * math.sin(0.5 * (theta2 - theta1)) / (9 * (3**0.5)) * (9 / 2)
    if x>=0:
        if (my2-oy2)<(yyy+0.05):
            ox=x
            oy=y
        else:
            ox = ox2
            oy = oy2 + r
        return (ox,oy)
    else:
        if (my1-oy1)<(yyy+0.05):
            ox = x
            oy = y
        else:
            ox = ox1
            oy = oy1 + r
        return (ox,oy)
