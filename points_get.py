import random


class points_get:

    # 维度
    dimension = 2

    # 点的数量
    p_num = 0

    point_dit = {
        "index": [],
        "data": [],
        "dimension": 2,
        "p_num": 0,
    }

    def __init__(self, dimension, p_num):
        self.point_dit["index"] = []
        self.point_dit["data"] = []
        self.point_dit["dimension"] = dimension
        self.point_dit["p_num"] = p_num
        for i in range(p_num):
            self.point_dit["index"].append(i)
            data = []
            for j in range(dimension):
                random.seed()
                rand = random.randint(1, 100)
                data.append(rand)
            self.point_dit["data"].append(data)
