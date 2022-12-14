import math

import numpy as np


# 用于解决超平面问题

class super_face:
    # 超平面点集
    x = []
    # 点
    point = []
    # 平面法向量
    w = []
    # 维度
    dimension = 0

    def __init__(self, x, point, dimension):
        self.x = np.asarray(x)
        self.point = np.asarray(point)
        self.dimension = dimension
        self.w = []

        # 初始化法向量
        vectors_points = []  # 用于生成向量的点
        for i in range(dimension):
            vectors_points.append(x[i])
        vectors = []  # 向量
        for i in range(len(vectors_points) - 1):
            vectors.append(np.subtract(x[i + 1], x[0]))
        # 用于生成法向量的坐标阵
        point_array = np.asarray(vectors)
        # print(f"用于生成法向量的坐标阵:\n{point_array}")
        # self.w.append(point_array[..., 1:])
        for i in range(self.dimension):
            matrix = np.concatenate((point_array[..., 0:i], point_array[..., i + 1:]), axis=1)
            self.w.append(np.linalg.det(matrix))
        self.w = np.asarray(self.w)
        # print(f"w:\n{self.w}")

    # 点到面的距离
    def p_distance(self, point=None):
        if point is None:
            point = self.point
        d_1 = np.vdot(self.w.T, np.subtract(point, self.x[0]))
        d_2 = np.linalg.norm(self.w)
        d = math.fabs(d_1/d_2)
        return d

    # 点位于超面的位置 + 上 0 中 - 下
    def p_place(self):
        return np.vdot(self.w.T, self.point) + self.p_distance()

    def p_shadow(self):
        zero = np.zeros(self.dimension)
        b = self.p_distance(zero)
        lamda = -(np.vdot(self.w, self.point.T) + b) / np.vdot(self.w, self.w.T)
        point_shadow = lamda * self.w + self.point
        return point_shadow

# a = super_face([[1, 2, 3], [2, 13, 4], [3, 4, 15]], [7, 7, 6], 3)
# print(a.p_distance())
# print(a.p_place())

b = super_face([[0,0,2], [2,0,0], [0,3,1], [1,3,0]], [0,3,0],3)
print(b.p_distance())
print(b.p_place())
