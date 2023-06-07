from math import erf, sqrt, exp, pi


class Distribution:
    def __init__(self):
        self.interval_row = dict()
        self.intervals = []
        self.n_sum = 0
        self.W = []
        self.middles = []
        self.Xv = 0
        self.N = []
        self.Dv = 0

    def set_interval_row(self, interval_row: dict):
        self.interval_row = interval_row
        self.intervals = list(self.interval_row.keys())
        self.N = list(self.interval_row.values())
        self.interval_row = interval_row
        self.n_sum = sum(interval_row.values())
        #W
        for ni in interval_row.values():
            self.W.append(ni / self.n_sum)
        #middles
        for a, b in interval_row.keys():
            self.middles.append((a + b) / 2)
        #Xv
        for i in range(len(self.middles)):
            self.Xv += self.middles[i] * self.N[i]

        self.Xv /= self.n_sum

        self.Dv = 0

        for i, xi in enumerate(self.middles):
            self.Dv += (xi - self.Xv) ** 2 * self.N[i]
        self.Dv /= self.n_sum

        self.sigma = self.Dv ** 0.5


        self.S = 0

        for i, xi in enumerate(self.middles):
            self.S += (xi - self.Xv) ** 2 * self.N[i]
        self.S /= self.n_sum - 1
        self.S = self.S ** 0.5
        self.h = list(self.interval_row.keys())[0][1] - list(self.interval_row.keys())[0][0]

        self.a = self.Xv

        self.sigma = self.Dv ** 0.5

    def get_normal_theoretical_probability(self, interval):
        t2 = (interval[1] - self.a) / self.sigma
        t1 = (interval[0] - self.a) / self.sigma
        return 0.5 * (erf(t2 / sqrt(2)) - erf(t1 / sqrt(2)))

    def get_normal_chi2(self):
        value = 0
        n = sum(self.N)
        for i in range(len(self.intervals)):
            npi = n * self.get_normal_theoretical_probability(self.intervals[i])
            value += ((self.N[i] - npi) ** 2 / npi)
        return value

    def process_normal_density(self, a, sigma):
        density = lambda x, a, sigma: (1 / (sqrt(2 * pi) * sigma)) * exp(-(((x - self.a) ** 2) / (2 * self.sigma ** 2)))
        x = [i for i in range(int(a) - 50, int(a) + 50)]
        y = [density(xi, a, sigma) for xi in x]
        return x, y