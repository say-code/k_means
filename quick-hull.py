import math
import random

import numpy as np
from points_get import points_get
from super_face import super_face
from scipy.spatial import ConvexHull
from scipy.spatial import distance as Distance
from pit_show import pit_show
import copy

"""
goal1 传入点并对点进行快速凸包，返回各个凸包超平面
    https://zhuanlan.zhihu.com/p/166105080
goal2 传入点和超平面，计算点到超平面的距离
    2-1 点到超平面距离
    https://blog.csdn.net/qq_22661171/article/details/107268634
    https://blog.csdn.net/wangyuanshun/article/details/88529773?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-88529773-blog-107268634.pc_relevant_multi_platform_whitelistv3&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1-88529773-blog-107268634.pc_relevant_multi_platform_whitelistv3&utm_relevant_index=1
    2-2 平面法向量
    https://zhuanlan.zhihu.com/p/37634441
    2-3 判断点位于超面的位置
    

"""


class quick_hull:
    # 点的数量
    p_num = 0
    # 维度
    dimension = 2
    # 点集
    points = []
    # 分类数量
    kind = 2
    # 类集
    kind_points = {}

    # # kind 分类数量 p_num 点的数量 dimension 维度
    def __init__(self, kind=2, p_num=50, dimension=2):
        self.points = points_get(dimension, p_num).point_dit["data"]
        self.p_num = p_num
        self.kind = kind
        self.dimension = dimension

        self.points_unique()
        self.dimension_init()
        self.show()
        temp = []
        self.group_init()
        self.classify()
        for i in range(15):
            # while temp != self.kind_points:

            self.group_init()
            self.classify2()
            print(i)
            self.show()

    # 1 生成点 & 排除重复点
    def points_unique(self):

        # 将点转换为np数组
        self.points = np.array(self.points)
        # print(self.points)
        # 排除重复点
        self.points = np.unique(self.points, axis=0).tolist()
        # print(self.points)

    # 2 根据维度为每个类初始化点（3维4个点，4维5个...)
    def dimension_init(self):
        # 请确保有足够的点
        temp = []
        # temp = self.points.copy()
        for i in range(self.kind):
            self.kind_points[i.__str__()] = {}
            self.kind_points[i.__str__()]["points"] = []
            for j in range(self.dimension + 1):
                rand = random.randint(0, len(self.points) - 1)
                while self.points[rand] in temp:
                    rand = random.randint(0, len(self.points) - 1)
                self.kind_points[i.__str__()]["points"].append(self.points[rand])
                temp.append(self.points[rand])
            # if i==0:

                # print(self.kind_points)

    # 3 对每个类进行高维凸包 返回每个凸包的索引
    def quick_hull_start(self, point_group=[]):
        # print(point_group)
        points = np.array(point_group)
        hull = ConvexHull(points)
        return (hull.simplices.tolist(), hull.vertices)

    def group_init(self):
        for i in self.kind_points.keys():
            self.kind_points[i]["arg_face"] = []
            self.kind_points[i]["arg_point"] = []
            (self.kind_points[i]["arg_face"], self.kind_points[i]["arg_point"]) = self.quick_hull_start(
                self.kind_points[i]["points"])
            self.kind_points[i]["face"] = []
            for j in range(len(self.kind_points[i]["arg_face"])):
                arg_face = self.kind_points[i]["arg_face"][j]
                self.kind_points[i]["face"].append([])
                for p in arg_face:
                    self.kind_points[i]["face"][j].append(self.kind_points[i]["points"][p])

    #     if len(point_group) < self.dimension + 1:
    #         raise Exception(f"传入数组数据过小！数组长度为{len(point_group)}\n\t数据为{point_group}")
    #     # # 初始化超体
    #     side_point = []  # 用于快速凸包的点集
    #     n_points = point_group.copy()  # 未被分配的点集合
    #     for i in range(self.dimension):
    #         rand = random.randint(0, len(n_points))
    #         side_point.append(n_points[rand])
    #         n_points.pop(rand)
    #     # # 初始化每个超面
    #     f = []
    #     f_ext = []
    #     for i in range(len(side_point)):
    #         temp = side_point.copy().pop(i)
    #         f.append(temp)
    #         f_ext.append([])
    #     print(f"初始化：目前已有的超面为{f}")
    #     for F in f:
    #         ps = n_points.copy()
    #         for i in range(len(ps)):
    #             if super_face(F, ps[i], self.dimension).p_place() > 0:
    #                 f_ext[i].append(ps[i])
    #                 n_points.remove(ps[i])
    #     # # 外部点集非空的面保存待定面集Q中
    #     q = []
    #     q_ext = []
    #     is_f = np.zeros(len(f))
    #     for i in range(len(f_ext)):
    #         if f_ext[i]:
    #             q.append(f[i])
    #             q_ext.append(f_ext[i])
    #             is_f[i] = 1
    #     # 用于判断面f是否被访问过
    #     for i in range(len(q)):
    #         F = q[i]
    #         q_ext_len = []
    #         for p in q_ext[i]:
    #             q_ext_len.append(super_face(F, p, self.dimension).p_distance())
    #         # 外部点集中最远的点在q_ext中索引值
    #         max_p = (np.array(q_ext_len)).argmax()
    #         v = [F]
    #         v_ext = [q_ext[i]]
    #         # --获取可见面集v中每个面的未被访问过的邻居面N，并保存在集合n中--
    #
    #         n = []
    #         for s in v:
    #             (res, arg) = get_N(f, is_f, s, self.dimension)
    #             for t in range(res):
    #                 N = res[t]
    #                 if N not in n:
    #                     n.append((arg[t], N))
    #                     is_f[arg[t]] = 1
    #         # --结束获取--
    #         for N in n:
    #             if super_face(q_ext[max_p], N[1], self.dimension).p_place() > 0:
    #                 v.append(N[1])
    #                 v_ext.append(f_ext[N[0]])
    #         # 把集合v中每个面的外部点汇集到一个点集l中
    #         l = v_ext
    #         # 集合V中所有面的临界便，构成一个集合h
    #         h = get_H(v, self.dimension)
    #         ns = [] # 新面集
    #         ns_ext = []
    #         for R in h:
    #             ns.append(R.append(q_ext[max_p]))
    #             ns_ext.append([])
    #         for F in ns:
    #             ls = l.copy()
    #             for pi in range(len(ls)):
    #                 if super_face(F, ls[pi], self.dimension).p_place() > 0:
    #                     l.remove(ls[pi])
    #                     ns_ext[pi].append(ls[pi])
    #         qq = q.copy()
    #         for Q in qq:
    #             if Q in v:
    #                 q.remove(Q)
    #         for F in ns:

    # 4 计算点到每个超平面的距离并归类
    def classify(self):
        # # 初始化一个新点集，排除所有凸包中的点
        n_points = self.points.copy()
        # n_points = []
        # for pp in self.kind_points.keys():
        #     # pd = np.array(pp["face"])
        #     arg_p = np.random.choice(self.kind_points[pp]["arg_point"], int(len(self.kind_points[pp]["arg_point"])/2))
        #     for p in arg_p:
        #         n_points.append(self.kind_points[pp]["points"][p])
        #         self.kind_points[pp]["points"][p]
        for i in self.kind_points.keys():
            self.kind_points[i]["points"] = []
            for face in self.kind_points[i]["face"]:
                for point in face:
                    if point not in self.kind_points[i]["points"]:
                        self.kind_points[i]["points"].append(point)
                    if point in n_points:
                        n_points.remove(point)

        for point in n_points:
            min_distance = float('inf')
            res = 1
            for i in self.kind_points.keys():
                for face in self.kind_points[i]["face"]:
                    sf = super_face(face, point, self.dimension)
                    point_shadow = sf.p_shadow()
                    ps = list(self.kind_points[i]["points"]).copy()
                    # print(point_shadow)
                    ps.append(point_shadow)
                    # print(self.kind_points[i]["points"])
                    if self.kind_points[i]["arg_face"] == ConvexHull(np.array(ps)).simplices.tolist():
                        distance = sf.p_distance()
                        if distance < min_distance:
                            min_distance = distance
                            res = i
                    else:
                        for fass in self.kind_points[i]["face"]:
                            for sp in fass:
                                distance = 0
                                for ia in range(self.dimension):
                                    distance = distance + math.pow(sp[ia] - point[ia], 2)
                                distance = math.sqrt(distance)
                                if distance < min_distance:
                                    min_distance = distance
                                    res = i

            self.kind_points[res]["points"].append(point)
            # print(self.kind_points)
        # print(self.kind_points)

    def classify2(self):
        # # 初始化一个新点集，排除所有凸包中的点
        # n_points = self.points.copy()
        n_points = []
        for pp in self.kind_points.keys():
            # pd = np.array(pp["face"])
            arg_p = np.random.choice(self.kind_points[pp]["arg_point"], int(len(self.kind_points[pp]["arg_point"])/2))
            temps = self.kind_points[pp]["points"].copy()
            for p in arg_p:
                n_points.append(self.kind_points[pp]["points"][p])
                if self.kind_points[pp]["points"][p] in temps:
                    temps.remove(self.kind_points[pp]["points"][p])
            self.kind_points[pp]["points"] = temps
        self.group_init()
        for point in n_points:
            min_distance = float('inf')
            res = 1
            for i in self.kind_points.keys():
                for face in self.kind_points[i]["face"]:
                    sf = super_face(face, point, self.dimension)
                    point_shadow = sf.p_shadow()
                    ps = list(self.kind_points[i]["points"]).copy()
                    # print(point_shadow)
                    ps.append(point_shadow)
                    # print(self.kind_points[i]["points"])
                    if self.kind_points[i]["arg_face"] == ConvexHull(np.array(ps)).simplices.tolist():
                        distance = sf.p_distance()
                        if distance < min_distance:
                            min_distance = distance
                            res = i
                    else:
                        for fass in self.kind_points[i]["face"]:
                            for sp in fass:
                                distance = 0
                                for ia in range(self.dimension):
                                    distance = distance + math.pow(sp[ia] - point[ia], 2)
                                distance = math.sqrt(distance)
                                if distance < min_distance:
                                    min_distance = distance
                                    res = i

            self.kind_points[res]["points"].append(point)

    # 5 第一次归类完成后开始循环选举（重复3，4）
    def show(self):
        show = pit_show()

        for i in self.kind_points.keys():
            x = []
            y = []
            for point in self.kind_points[i]["points"]:
                x.append(point[0])
                y.append(point[1])

            show.append(x, y, "block" + i)
        show.show()


# 寻找邻居面 || f 所有面 | face 被寻找的面
def get_N(f, is_f, face, dimension):
    n = []
    arg_n = []
    # 如果两个面中有至少（维度数）个点重合，且这几个点相邻，那么这两个面是相邻的
    for k in range(f):
        if is_f[k] != 0:
            continue
        F = f[k]
        if F == face:
            continue
        # 寻找 F 与 face 的最长连续子序列，并且值为 维度值
        for point in F:
            if point in face:
                index_list = np.where(np.array(face) == point)
                flag = True
                for index in index_list:
                    for i in range(dimension):
                        place_F = (index + i) % len(F)
                        place_face = (index + i) % len(face)
                        if F[place_F] != face[place_face]:
                            flag = False
                            break
                    if not flag:
                        continue
                    else:
                        n.append(F)
                        arg_n.append(k)
                        break
                if flag:
                    break
    if not n:
        raise Exception("我找不到相邻的面，你看看怎么回事嘞")
    return n


# 寻找临界边 遍历所有面，将面的边提取到sides集合中，集合中没有重复的边都是临界边
def get_H(f, dimension):
    sides = []
    for F in f:
        for i in range(len(F)):
            side = []
            for j in range(dimension):
                side.append(F[(i + j) % len(F)])
            side.sort()
            sides.append(side)

    arr = np.array(sides)
    key = np.unique(arr)
    res = []
    for k in key:
        v = arr[arr == k].size
        if v == 1:
            res.append(k)
    return res

def get_distance(p1, p2):
    distance = 0
    for i in range(p1):
        distance += math.pow(p1[i]-p2[i], 2)
    return distance

asd = quick_hull(3, 100, 2)
# print(asd.points)
# asd.quick_hull_start(asd.points)
