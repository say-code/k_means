import matplotlib.pyplot as plt


class pit_show:

    def __init__(self):
        self.fig, self.ax = plt.subplots()

    def append(self, x, y, label=""):
        self.ax.scatter(x, y, label=label)

    def show(self):
        self.ax.legend()
        plt.show()
