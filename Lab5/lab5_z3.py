import matplotlib.pyplot as plt
from collections import defaultdict
from prettytable import PrettyTable
import warnings
warnings.filterwarnings("ignore")
import matplotlib
matplotlib.use('Qt5Agg')


class Distribution:
    def __init__(self, row=[23, 29, 35, 7, 11, 18, 23, 30, 36, 18, 11, 8, 13, 20, 25, 27, 14, 30, 20, 20, 24, 19, 21, 26, 22, 16, 26, 25, 33, 27], amount_intervals=6):
        # self.row = row if row else self.read_row()
        # self.var_row = self.get_var_row()
        self.amount_intervals = amount_intervals
        self.interval_row = self.read_interval_row()
        self.stat_frequency = self.get_stat_frequency()
        self.n = sum(self.stat_frequency.values())
        self.stat_relative_frequency = self.get_stat_relative_frequency()
        self.distribution_func = self.get_distribution_func()
        self.x_selective = self.get_x_selective()
        self.variance = self.get_variance()
        self.standard_deviation = self.get_standard_deviation()
        self.corrected_standard_deviation = self.get_corrected_standard_deviation()
        # self.create_func_graph()
        # self.create_frequency_polygon()
        # self.crate_relative_frequency_polygon()
        # self.create_bar_plot()

    def read_interval_row(self, console=True):
        interval_row = dict()
        if console:
            vars = list(map(float, input("Введите границы интервалов через точку с запятой: ").split(';')))
            values = list(map(float, input("Введите значения интервалов через точку с запятой: ").split(';')))
            if len(vars) != len(values) + 1:
                print("Количество интервалов не соответствует количествву значений")
            for i in range(len(values)):
                interval_row[(vars[i], vars[i + 1])] = values[i]
        else:
            with open("z3_var23.txt") as f:
                string = f.readline()
                vars = [tuple(map(float, i.split(";"))) for i in string.split(" ")]
                values = list(map(int, f.readline().split()))
                for i in range(len(vars)):
                    interval_row[vars[i]] = values[i]
        return interval_row

    def get_stat_frequency(self):
        return {key: value for key, value in self.interval_row.items()}

    def get_stat_relative_frequency(self):
        return {key: value / self.n for key, value in self.interval_row.items()}

    def get_distribution_func(self):
        distribution_func = dict()
        minimum = float('-inf')
        frequency = 0
        for value, relative_frequency in self.stat_relative_frequency.items():
            distribution_func[frequency] = (minimum, value[1])
            minimum = value[1]
            frequency += relative_frequency
        distribution_func[frequency] = (minimum, '+inf')
        return distribution_func

    def get_x_selective(self):
        return sum([(value[0] + value[1]) / 2 * frequency for value, frequency in self.stat_frequency.items()]) / self.n

    def get_variance(self):
        return sum([frequency * ((value[0] + value[1]) / 2 - self.x_selective) ** 2 for value, frequency in self.stat_frequency.items()])

    def get_standard_deviation(self):
        return self.variance ** 0.5

    def get_corrected_standard_deviation(self):
        return (self.variance * self.n / (self.n - 1)) ** 0.5

    def create_func_graph(self):
        fig, ax = plt.subplots(1, 1)
        a = min(list(self.stat_frequency.keys())[0][0], 0) - 2
        b = list(self.stat_frequency.keys())[0]
        ax.plot((min(list(self.stat_frequency.keys())[0][0], 0) - 2, list(self.stat_frequency.keys())[0][1]), (0, 0),
                color='b')
        for part in list(self.distribution_func.items())[1:-1]:
            x1, y1 = (part[1][0], part[0])
            x2, y2 = part[1][1], part[0]
            ax.plot((x1, x2), (y1, y2), color='b')
        ax.plot((list(self.stat_frequency.keys())[-1][1], list(self.stat_frequency.keys())[-1][1] + 2), (1, 1),
                color='b')
        x_axes = [i[0] for i in self.distribution_func.values()]
        ax.plot(x_axes[1:], [key for key in self.distribution_func.keys()][1:], 'bo')
        ax.plot(x_axes[1:], [key for key in self.distribution_func.keys()][1:], 'w.')
        # lx = list(self.distribution_func.items())[0][1][0]
        # rx = list(self.distribution_func.items())[-1][1][1]
        # #
        # ax.set_xbound(lx, rx)
        ax.set_ybound(0, 1.1)
        ax.set_xlabel('x')
        ax.set_ylabel('F*(x)')
        ax.grid(True)
        plt.subplot(1, 1, 1)
        # x = [key[1] for key in self.stat_frequency.keys()]
        # x = [min(x[0] - abs(x[0] * 1), 0)] + x + [x[-1] + 1]
        # y = list(self.distribution_func.keys()) + [1]
        # plt.step(x, y, where='post')
        # plt.scatter(x[1:-1], y[1:-1], marker='o', facecolors='white', edgecolors='blue', zorder=10)
        # plt.xticks(x[:-1])
        # plt.yticks([i * 0.1 for i in range(11)])
        # plt.xlabel('x')
        # plt.ylabel('F*(x)')
        # plt.show()

    def create_frequency_polygon(self):
        fig, ax = plt.subplots(1, 1)
        x = [round((key[0] + key[1]) / 2, 2) for key in self.stat_frequency.keys()]
        y = list(self.stat_frequency.values())
        ax.plot(x, y)
        ax.set_xbound(0, round(max(x) * 1.1))
        ax.set_ybound(0, round(max(y) * 1.1))
        # ax.xticks([0] + x)
        # ax.yticks([0] + y)
        ax.scatter(x, y)
        ax.set_xlabel('x')
        ax.set_ylabel('ni')
        ax.grid(True)
        plt.subplot(1, 1, 1)
        # x = [round((key[0] + key[1]) / 2, 2) for key in self.stat_frequency.keys()]
        # y = list(self.stat_frequency.values())
        # plt.plot(x, y)
        # plt.xlim([0, max(x) * 2])
        # plt.ylim([0, max(y) * 2])
        # plt.xticks([0] + x)
        # plt.yticks(range(round(min(min(y), 0), 2), round(max(y) * 2), 2))
        # plt.scatter(x, y)
        # plt.xlabel('x')
        # plt.ylabel('ni')
        # plt.show()

    def create_relative_frequency_polygon(self):
        fig, ax = plt.subplots(1, 1)
        x = [round((key[0] + key[1]) / 2, 2) for key in self.stat_relative_frequency.keys()]
        y = list(self.stat_relative_frequency.values())
        ax.plot(x, y)
        ax.set_xbound(0, round(max(x) * 1.1))
        ax.set_ybound(0, 1)
        # ax.xticks([0] + x)
        # ax.yticks([i * 0.1 for i in range(11)])
        ax.scatter(x, y)
        ax.set_xlabel('x')
        ax.set_ylabel('ni/n')
        ax.grid(True)
        plt.subplot(1, 1, 1)
        # x = [round((key[0] + key[1]), 2) / 2 for key in self.stat_relative_frequency.keys()]
        # y = list(self.stat_relative_frequency.values())
        # plt.plot(x, y)
        # plt.xlim([0, max(x) * 2])
        # plt.ylim([0, 1])
        # plt.xticks(x)
        # plt.yticks([i * 0.1 for i in range(11)])
        # plt.scatter(x, y)
        # plt.xlabel('x')
        # plt.ylabel('ni/n')
        # plt.show()

    def create_bar_plot(self):
        fig, ax = plt.subplots(1, 1)
        first = list(self.stat_frequency.keys())[0]
        x = [key[0] for key in self.stat_frequency.keys()] + [max(self.stat_frequency.keys(), key=lambda x: x[1])[1]]
        y = [value / (key[1] - key[0]) for key, value in self.stat_frequency.items()]
        ax.bar(x[:-1], y, width=(first[1] - first[0]), align='edge')
        ax.set_xticks(x)
        ax.set_yticks(y)
        ax.set_xlabel('x')
        ax.set_ylabel('ni/h')
        ax.grid(True)
        plt.subplot(1, 1, 1)
        # first = list(self.stat_frequency.keys())[0]
        # x = [key[0] for key in self.stat_frequency.keys()] + [max(self.stat_frequency.keys(), key=lambda x: x[1])[1]]
        # y = [value / (key[1] - key[0]) for key, value in self.stat_frequency.items()]
        # plt.bar(x[:-1], y, width=(first[1] - first[0]), align='edge')
        # plt.xticks(x)
        # plt.yticks(y)
        # plt.xlabel('x')
        # plt.ylabel('ni/h')
        # plt.show()


def show_help():
    print("1. Справка\n2. Выход\n3. Получить все данные\n4. Варианционный ряд\n"
          "5. Статистический ряд частот, относительных частот и их графики\n6. Эмпирическая функция распределения и ее график\n"
          "7. Числовые характеристики")


def show_frequencies_row(dist: Distribution):
    print(f"Статистический ряд частот:\n")
    x = PrettyTable()
    x.add_row(["Xi;Xi+1"] + list(map(str, dist.stat_frequency.keys())))
    x.add_row(["Ni"] + list(map(str, dist.stat_frequency.values())))
    print(x.get_string(header=False))
    print()
    print(f"Статистический ряд относительных частот:\n")
    x = PrettyTable()
    x.add_row(["Xi;Xi+1"] + list(map(str, dist.stat_relative_frequency.keys())))
    x.add_row(["Ni/N"] + list(map(str, dist.stat_relative_frequency.values())))
    print(x.get_string(header=False))
    dist.create_frequency_polygon()
    dist.create_relative_frequency_polygon()
    dist.create_bar_plot()


def show_func(dist: Distribution):
    print("F*(x) = ")
    for key, value in sorted(dist.distribution_func.items(), key=lambda x: x[0]):
        if 0.99 <= key:
            print(f"{key}, при x ∈ ({value[0]}; {value[1]})")
        else:
            print(f"{key}, при x ∈ ({value[0]}; {value[1]}]")
    dist.create_func_graph()


def show_characteristics(dist: Distribution):
    print(f"Xв = Σ(i=1, n)((Ni * Xi)/N) = {dist.x_selective}")
    print()
    print(f"Dв = Σ(i=1, n)(Ni * ((Xi-Xв) ^ 2))/N) = {dist.variance}")
    print()
    print(f"σв = sqrt(Dв) = {dist.standard_deviation}")
    print()
    print(f"S = sqrt(n / (n - 1) * Dв) = {dist.corrected_standard_deviation}")


def show_all(dist: Distribution):
    show_frequencies_row(dist)
    print()
    show_func(dist)
    print()
    show_characteristics(dist)
    plt.show()


if __name__ == "__main__":
    dist = Distribution()
    print("Выберите нужный вариант:")
    show_help()
    while True:
        value = int(input("Нужный вариант: "))
        if value == 1:
            show_help()
        if value == 2:
            exit()
        if value == 3:
            show_all(dist)
        if value == 4:
            show_frequencies_row(dist)
        if value == 5:
            show_func(dist)
        if value == 6:
            show_characteristics(dist)

