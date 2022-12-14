import math
import random

from pit_show import pit_show
from points_get import points_get
from graham_scan import convex_hull_get, get_circle_center,get_side


# print(point_dit)

class k_means:
    res = []
    # 创建分类
    record_point = []
    true_point = []

    def __init__(self, kind=2, p_num=50, dimension=2):
        self.kind = kind
        self.dimension = dimension
        self.point_dit = points_get(dimension, p_num).point_dit.copy()
        for j in range(kind):
            # 从point_dit中随便选取一个点
            rand = random.randint(0, len(self.point_dit["data"]) - 1)
            rand_res = self.point_dit["data"][rand]
            # 如果rand_res 已经再record_check 出现过，则重新选择，直到不重复为止
            while rand_res in self.record_point:
                rand = random.randint(0, len(self.point_dit["data"]))
                rand_res = self.point_dit["data"][rand]
            self.record_point.append(rand_res)
            self.true_point.append([])

        # 创建维度并初始化第一个点
        for i in range(dimension):
            self.res.append([])
            for data in self.record_point:
                self.res[i].append(data[i])

        temp_point = []
        # temp_kind = self.kind
        # while temp_point != self.record_point and self.kind > 2:
            # temp_point = self.record_point.copy()


            # self.classification()
            # self.election()
            # self.election_by_convex_hull_2d()

        i = 0
        for point in self.record_point:
            self.true_point[i].append(point)
            i = i + 1
        i = 0
        while temp_point != self.true_point and self.kind == kind and i != 50:
            temp_point = self.true_point.copy()
            self.election_by_side()
            i += 1



    def calc_point_distance(self, point1=None, point2=None):
        if point2 is None:
            point2 = [0]
        if point1 is None:
            point1 = [0]
        length = 0
        for i in range(len(point1)):
            x1 = point1[i]
            x2 = point2[i]
            # print("calc_point_distance", length,x1,x2)
            length = length + math.pow(abs(x1 - x2), 2)

        return math.pow(length, 0.5)

    # 整理并展示（仅限于二维）
    def show(self):
        show = pit_show()

        for i in range(self.kind):
            x = []
            y = []
            for point in self.true_point[i]:
                x.append(point[0])
                y.append(point[1])

            show.append(x, y, "block" + i.__str__())
        show.show()

    # 归类
    def classification(self):
        for i in range(self.kind):
            self.true_point[i] = []
        for point in self.point_dit["data"]:
            # 计算距离
            min_point = 0
            min_point_res = float("inf")
            for i in range(self.kind):
                # print("classification", self.record_point)
                father_point = self.record_point[i]
                distance = self.calc_point_distance(father_point, point)
                if distance < min_point_res:
                    min_point = i
                    min_point_res = distance

            self.true_point[min_point].append(point)

    # 选举
    def election(self):
        for i in range(self.kind):
            new_point = []
            length = len(self.true_point[i])
            for j in range(self.dimension):
                ev_sum = 0
                for point in self.true_point[i]:
                    ev_sum = ev_sum + point[j]
                ev_sum = ev_sum / length
                new_point.append(ev_sum)

            self.record_point[i] = new_point

        # print(self.record_point)

    # 通过凸包选举(2d)
    def election_by_convex_hull_2d(self):
        for i in range(self.kind):
            if len(self.true_point[i]) == 0:
                self.true_point.pop(i)
                self.kind = self.kind - 1
                break
            if len(self.true_point[i]) == 1:
                self.record_point[i] = self.true_point[i][0]
            else:
                point_list = convex_hull_get(self.true_point[i])
                # print(point_list)
                point = get_circle_center(point_list)
                # print(point)
                self.record_point[i] = point

        # print(self.record_point)

    #通过边选取
    def election_by_side(self):
        temp_point1 = self.true_point.copy()
        # print(temp_point1)
        for i in range(self.kind):
            self.true_point[i] = []
        for point in self.point_dit["data"]:
            min_ins = float('inf')
            min_kind = 0
            for i in range(self.kind):
                if len(temp_point1[i]) == 0:
                    self.true_point = temp_point1.pop(i)
                    self.kind = self.kind - 1

                    break
                if len(temp_point1[i]) == 1:
                    ins = self.calc_point_distance(point, temp_point1[i][0])
                else:
                    # print('temp_point', temp_point1[i])
                    points = convex_hull_get(temp_point1[i])
                    ins = get_side(point, points)
                if ins < min_ins:
                    min_ins = ins
                    min_kind = i
            self.true_point[min_kind].append(point)





if __name__ == '__main__':
    km = k_means(kind=4, p_num=50, dimension=2)
    km.show()
