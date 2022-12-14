import math

from scipy.linalg import solve
import numpy as np


# 生成凸包列表
def convex_hull_get(points=None):
    a4 = sorted(points)
    points = [e for i, e in enumerate(a4) if e not in a4[:i]]
    if points is None:
        points = [(1, 2), (2, 3)]
    print("convex_hull_get", points)
    left_point = min(points, key=lambda ii: (ii[0], ii[1]))
    right_point = max(points, key=lambda ii: (ii[0], ii[1]))
    # 初始化下凸壳
    downs = [right_point, left_point]
    # 初始化上凸壳
    ups = [left_point, right_point]

    # print(downs, ups)

    # 划分上下壳
    # dels记录共线的点
    # delss = []
    for point in points:
        res = is_up(left_point, right_point, point)
        if res > 0:
            ups.append(point)
        elif res < 0:
            downs.append(point)
        # else:
        # delss.append(point)

    # for dels in delss:
    # points.remove(dels)

    # 分别按x轴排序
    downs.sort(key=lambda ii: (ii[0], ii[1]))
    ups.sort(key=lambda ii: (ii[0], ii[1]), reverse=False)

    # 对downs进行凸包
    if len(downs) >= 4:
        i = 2
        while i != len(downs) - 2 and i != 2:
            (pa, pb) = re_side(downs[i], downs[i - 1], downs[i + 1])
            res = is_clockwise(pa, pb)
            if res >= 0:
                downs.pop(i)
                i = i - 1
            else:
                i = i + 1
    # print("a"+downs.__str__())
    # 对ups进行凸包
    if len(ups) >= 4:
        i = 2
        while i != len(downs) - 2 and i != 2:
            (pa, pb) = re_side(downs[i], downs[i - 1], downs[i + 1])
            res = is_clockwise(pa, pb)
            if res <= 0:
                downs.pop(i)
                i = i - 1
            else:
                i = i + 1

    # print(downs)
    # 拼接downs和ups
    return downs + ups[1:-2]


# 判断上下
def is_up(left_point, right_point, point):
    (x, y) = point
    (x1, y1) = left_point
    (x2, y2) = right_point
    return x / (x2 - x1) + y / (y1 - y2) - x1 / (x2 - x1) + y1 / (y2 - y1)


# 判断顺逆
def is_clockwise(p0_1, p1_2):
    return p0_1[0] * p1_2[1] - p0_1[1] * p1_2[0]


# 快速生成两条向量
def re_side(p_index, p1, p2):
    return (p1[0] - p_index[0], p1[1] - p_index[1]), (p2[0] - p_index[0], p2[1] - p_index[1])

# --- 以下为边最近 ---
def get_side(point, points):
    min_ins = float('inf')
    for i in range(len(points)-1):
        sideA = (point[0] - points[i][0], point[1] - points[i][1])
        sideB = (points[i+1][0] - points[i][0], points[i+1][0] - points[i][0])
        c = sideA[0] * sideB[0] + sideA[1] * sideB[0]
        cm = sideB[0] * sideB[0] + sideB[1] * sideB[1]
        # if cm == 0:
        #     continue
        if cm <= 0:
            return math.sqrt(sideA[0] * sideA[0] + sideA[1] * sideA[1])
        elif cm >= 1:
            return math.sqrt(math.pow(point[0] - points[i+1][0],2) + math.pow(point[1] - points[i+1][1],2))
        res = c / cm
        e = (sideA[0] - res * sideB[0], sideA[1] - res * sideB[1])
        ins = e[0] * e[0] + e[1] * e[1]
        if ins < min_ins:
            min_ins = ins

    sideA = (point[0] - points[-1][0], point[1] - points[-1][1])
    sideB = (points[0][0] - points[-1][0], points[0][0] - points[-1][0])
    c = sideA[0] * sideB[1] + sideA[1] * sideB[0]
    cm = sideB[0] * sideB[0] + sideB[1] * sideB[1]
    # if cm == 0:
    #     return min_ins
    res = c / cm
    e = (sideA[0] - res * sideB[0], sideA[1] - res * sideB[1])
    ins = e[0] * e[0] + e[1] * e[1]
    if ins < min_ins:
        min_ins = ins
    return min_ins


# --- 以下为外接圆圆心相关 ---
def get_circle_center(points):
    lp = len(points)
    if lp == 2:
        return (points[0][0] + points[1][0]) / 2, (points[0][1] + points[1][1]) / 2
    r = 0
    point = (-1, -1)
    for i in range(lp - 2):
        for j in range(i + 1, lp - 1):
            for k in range(j + 1, lp):
                if points[i] == points[j] or points[j] == points[k] or points[i] == points[k]:
                    continue
                point_temp, r_temp = calc_circle(points[i], points[j], points[k])
                if r_temp > r:
                    r = r_temp
                    point = point_temp
    if point[0] < 0 or point[1] < 0 or point[0] > max(points, key=lambda ii: ii[0])[0] or point[1] > \
            max(points, key=lambda ii: ii[1])[1]:
        x_sum = 0
        y_sum = 0
        for res in points:
            x_sum = x_sum + res[0]
            y_sum = y_sum + res[1]
        x_sum = x_sum / len(points)
        y_sum = y_sum / len(points)
        point = (x_sum, y_sum)
    print("get_circle_center:" + point.__str__())
    return point


# 计算圆心与半径
# http://www.zzvips.com/article/130432.html
# https://blog.csdn.net/ztf312/article/details/89197684
def calc_circle(A, B, C):
    xa, ya = A[0], A[1]
    xb, yb = B[0], B[1]
    xc, yc = C[0], C[1]

    # 两条边的中点
    x1, y1 = (xa + xb) / 2.0, (ya + yb) / 2.0
    x2, y2 = (xb + xc) / 2.0, (yb + yc) / 2.0

    # 两条线的斜率
    ka = (yb - ya) / (xb - xa) if xb != xa else None
    kb = (yc - yb) / (xc - xb) if xc != xb else None

    alpha = np.arctan(ka) if ka != None else np.pi / 2
    beta = np.arctan(kb) if kb != None else np.pi / 2

    # 两条垂直平分线的斜率
    k1 = np.tan(alpha + np.pi / 2)
    k2 = np.tan(beta + np.pi / 2)
    if k1 == k2:
        return (-1, -1), 0
    # 圆心
    # print([[1.0, -k1], [1.0, -k2]], [y1 - k1 * x1, y2 - k2 * x2])
    y, x = solve([[1.0, -k1], [1.0, -k2]], [y1 - k1 * x1, y2 - k2 * x2])
    # 半径
    r1 = np.sqrt((x - xa) ** 2 + (y - ya) ** 2)

    return (x, y), r1
