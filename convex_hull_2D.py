from  k_means import k_means


class convex_hull(k_means):
    def __init__(self, kind=2, p_num=50, dimension=2):
        super().__init__(kind, p_num, dimension)

