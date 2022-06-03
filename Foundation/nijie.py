import math
import Foundation.zhengjie as zhengjie

def nijie(x,y) -> list:
    r=9.0
    a=9.0
    rtheta1 = 361
    rtheta2 = 361
    if x>0:
        o=[x,y-r]
        bbo = (pow(o[0], 2) + pow(o[1], 2))**0.5
        jbbao = math.acos((r * r + r * r - bbo * bbo) / (2.0 * r * r))
        if o[1]>0:
            jbbab = (((jbbao * 180.0 / math.pi) + 30.0) / 180.0) * math.pi
        else:
            jbbab = ((30.0 - (jbbao * 180.0 / math.pi)) / 180.0) * math.pi
        bbb =((r * r + 3.0 * r * r - 2.0 * r * ((3.0)**0.5) * r * math.cos(jbbab)))**0.5
        jbbba = math.acos((pow(bbb, 2) + r * r - 3.0 * r * r) / (2.0 * r * bbb))
        jobbd = math.atan(math.fabs(o[1]) / math.fabs(o[0]))
        jobba = math.acos((bbo * bbo + r * r - r * r) / (2.0 * r * bbo))
        jbbbo = math.acos((bbb * bbb + bbo * bbo - r * r) / (2.0 * bbb * bbo))
        theta1 = jobbd - jbbbo - jbbba
        theta2 = 2 * jbbba + theta1
        (ox,oy)= zhengjie.zhengjie(theta1 / math.pi * 180.0, theta2 / math.pi * 180.0)
        if math.fabs((ox - x) * (ox - x) + (oy - y) * (oy - y))< 0.02:
            rtheta1 = theta1 / math.pi * 180.0
            rtheta2 = theta2 / math.pi * 180.0
            # print(rtheta1, rtheta2)
        jobbd = math.acos((x * x + bbo * bbo - (y - r) * (y - r)) / (2.0 *x* bbo))
        jobba = 1.0 / 2.0 * ( math.pi  - math.acos((r * r + r * r - bbo * bbo) / (2.0 * r * r)))
        theta1 = jobbd - jobba
        theta2 = 2.0 * jbbba + theta1
        (ox, oy) = zhengjie.zhengjie(theta1 / math.pi * 180.0, theta2 / math.pi * 180.0)
        if math.fabs((ox - x) * (ox - x) + (oy - y) * (oy - y)) < 0.02:
            rtheta1 = theta1 / math.pi * 180.0
            rtheta2 = theta2 / math.pi * 180.0
        x_x = x
        y_y = y

        b = 9.0*(3.0**0.5)
        theta1 = math.acos(x_x / (x_x * x_x + y_y * y_y)**0.5) - math.acos((a * a + x_x * x_x + y_y * y_y - b * b) / (2.0 * a * (x_x * x_x + y_y * y_y)**0.5))
        theta2 = math.acos(x_x / (x_x * x_x + y_y * y_y)**0.5) + math.acos( (a * a + x_x * x_x + y_y * y_y - b * b) / (2.0 * a * (x_x * x_x + y_y * y_y)**0.5))
        (ox, oy) = zhengjie.zhengjie(theta1 / math.pi * 180.0, theta2 / math.pi * 180.0)
        if math.fabs((ox - x) * (ox - x) + (oy - y) * (oy - y)) < 0.02:
            rtheta1 = theta1 / math.pi * 180.0
            rtheta2 = theta2 / math.pi * 180.0
    else:
        o = [x, y - r]
        bbo = (pow(o[0], 2) + pow(o[1], 2)) ** 0.5
        jbbao = math.acos((r * r + r * r - bbo * bbo) / (2.0 * r * r))
        if o[1] > 0:
            jbbab = (((jbbao * 180 / math.pi) + 30) / 180) * math.pi
        else:
            jbbab = ((30.0 - (jbbao * 180.0 / math.pi)) / 180.0) * math.pi
        jbbaao =  math.acos((r * r + r * r - bbo * bbo) / (2 * r * r))
        jobbaa = 0.5 * ( math.pi - jbbaao)
        jbbaab = jbbaao + 1.0 / 6.0
        bbb = ((r * r + 3.0 * r * r - 2.0 * r * ((3.0)**0.5) * r *  math.cos(jbbab)))**0.5
        jbbba =  math.acos((r * r + bbb * bbb - 3.0 * r * r) / (2.0 * r * bbb))
        jbbbo =  math.acos((bbb * bbb + bbo * bbo - r * r) / (2.0 * bbb * bbo))
        jobbd =  math.acos((x * x + bbo * bbo - (y - r) * (y - r)) / (2.0 * (-x) * bbo))
        theta1 = math.pi - jobbd - jbbba + jbbbo
        theta2 = 2.0 * jbbba + theta1
        (ox, oy) = zhengjie.zhengjie(theta1 / math.pi * 180.0, theta2 / math.pi * 180.0)
        if math.fabs((ox - x) * (ox - x) + (oy - y) * (oy - y)) < 0.02:
            rtheta1 = theta1 / math.pi * 180.0
            rtheta2 = theta2 / math.pi * 180.0
        jobbd =  math.acos((x * x + bbo * bbo - (y - r) * (y - r)) / (2.0 * (-x) * bbo))
        theta2 = jobbaa - jobbd +  math.pi
        theta1 = theta2 - 2.0 * jbbba
        (ox, oy) = zhengjie.zhengjie(theta1 / math.pi * 180.0, theta2 / math.pi * 180.0)
        if math.fabs((ox - x) * (ox - x) + (oy - y) * (oy - y)) < 0.02:
            rtheta1 = theta1 / math.pi * 180.0
            rtheta2 = theta2 / math.pi * 180.0
        x_x =x
        y_y =y
        b = 9.0 * (3.0)**0.5
        theta1 =  math.acos(x_x /(x_x * x_x + y_y * y_y)**0.5) - math.acos( (a * a + x_x * x_x + y_y * y_y - b * b) / (2.0 * a * (x_x * x_x + y_y * y_y)**0.5))
        theta2 =  math.acos(x_x / (x_x * x_x + y_y * y_y)**0.5) + math. acos((a * a + x_x * x_x + y_y * y_y - b * b) / (2.0 * a * (x_x * x_x + y_y * y_y)**0.5))
        (ox, oy) = zhengjie.zhengjie(theta1 / math.pi * 180.0, theta2 / math.pi * 180.0)
        if math.fabs((ox - x) * (ox - x) + (oy - y) * (oy - y)) < 0.02:
            rtheta1 = theta1 / math.pi * 180.0
            rtheta2 = theta2 / math.pi * 180.0
    if rtheta1>360 or rtheta2>360:
        rtheta1=None
        rtheta2=None
        raise ArithmeticError("Can't reach")
    #print(rtheta1, rtheta2)
    return [rtheta1,rtheta2]