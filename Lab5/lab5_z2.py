import matplotlib.pyplot as plt
from collections import defaultdict
from prettytable import PrettyTable
import warnings
warnings.filterwarnings("ignore")


class Distribution:
    def __init__(self, row=[23, 29, 35, 7, 11, 18, 23, 30, 36, 18, 11, 8, 13, 20, 25, 27, 14, 30, 20, 20, 24, 19, 21, 26, 22, 16, 26, 25, 33, 27], amount_intervals=6):
        self.row = row if row else self.read_row()
        self.var_row = self.get_var_row()
        self.amount_intervals = amount_intervals
        self.interval_row = self.get_interval_row()
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

    def read_row(self):
        return [float(i) for i in open("z2_var23.txt").readline().split(" ")]

    def get_var_row(self):
        return sorted(self.row)

    def get_interval_row(self):
        var_range = self.var_row[-1] - self.var_row[0]
        interval_value = round(var_range / (self.amount_intervals - 1), 2)
        intervals = []
        c = round(self.var_row[0] + 0.5 * interval_value, 2)
        intervals.append((round(self.var_row[0] - 0.5 * interval_value, 2), c))
        for i in range(1, self.amount_intervals):
            intervals.append((c, c + interval_value))
            c += interval_value
        interval_row = defaultdict(list)
        k = 0
        for i in self.var_row:
            if not (intervals[k][0] <= i <= intervals[k][1]):
                k += 1
            interval_row[(intervals[k][0], intervals[k][1])].append(i)
        return interval_row

    def get_stat_frequency(self):
        return {key: len(value) for key, value in self.interval_row.items()}

    def get_stat_relative_frequency(self):
        return {key: len(value) / self.n for key, value in self.interval_row.items()}

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
        return sum([frequency * ((value[0] + value[1]) / 2 - self.x_selective) ** 2 for value, frequency in self.stat_frequency.items()]) / self.n

    def get_standard_deviation(self):
        return self.variance ** 0.5

    def get_corrected_standard_deviation(self):
        return (self.variance * self.n / (self.n - 1)) ** 0.5

    def create_func_graph(self):
        x = [key[1] for key in self.stat_frequency.keys()]
        x = [min(x[0] - 1, 0)] + x + [x[-1] + 1]
        y = list(self.distribution_func.keys()) + [1]
        plt.step(x, y, where='post')
        plt.scatter(x[1:-1], y[1:-1], marker='o', facecolors='white', edgecolors='blue', zorder=10)
        plt.xticks(x[:-1])
        plt.yticks([i * 0.1 for i in range(11)])
        plt.xlabel('x')
        plt.ylabel('F*(x)')
        plt.show()

    def create_frequency_polygon(self):
        x = [round((key[0] + key[1]) / 2, 2) for key in self.stat_frequency.keys()]
        y = list(self.stat_frequency.values())
        plt.plot(x, y)
        plt.xlim([0, max(x) * 1.1])
        plt.ylim([0, max(y) * 1.1])
        plt.xticks([0] + x)
        plt.yticks([0] + y)
        plt.scatter(x, y)
        plt.xlabel('x')
        plt.ylabel('ni')
        plt.show()

    def create_relative_frequency_polygon(self):
        x = [round((key[0] + key[1]) / 2, 2) for key in self.stat_relative_frequency.keys()]
        y = list(self.stat_relative_frequency.values())
        plt.plot(x, y)
        plt.xlim([0, max(x) * 1.1])
        plt.ylim([0, 1])
        plt.xticks(x)
        plt.yticks([i * 0.1 for i in range(11)])
        plt.scatter(x, y)
        plt.xlabel('x')
        plt.ylabel('ni/n')
        plt.show()

    def create_bar_plot(self):
        first = list(self.stat_frequency.keys())[0]
        x = [key[0] for key in self.stat_frequency.keys()] + [max(self.stat_frequency.keys(), key=lambda x: x[1])[1]]
        y = [value / (key[1] - key[0]) for key, value in self.stat_frequency.items()]
        plt.bar(x[:-1], y, width=(first[1] - first[0]), align='edge')
        plt.xticks(x)
        plt.yticks(y)
        plt.xlabel('x')
        plt.ylabel('ni/h')
        plt.show()


def show_help():
    print("1. Справка\n2. Выход\n3. Получить все данные\n4. Варианционный ряд\n"
          "5. Статистический ряд частот, относительных частот и их графики\n6. Эмпирическая функция распределения и ее график\n"
          "7. Числовые характеристики")


def show_var_row(dist: Distribution):
    print(f"Вариационный ряд:\n{', '.join(map(str, dist.var_row))}")


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
    show_var_row(dist)
    print()
    show_frequencies_row(dist)
    print()
    show_func(dist)
    print()
    show_characteristics(dist)


if __name__ == "__main__":
    dist = Distribution(row=None)
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
            show_var_row(dist)
        if value == 5:
            show_frequencies_row(dist)
        if value == 6:
            show_func(dist)
        if value == 7:
            show_characteristics(dist)

