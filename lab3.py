from math import factorial, prod, pi, sqrt, exp


def combinations(n, k):
    return factorial(n) / (factorial(n - k) * factorial(k))


def bernoulli(p, n, m):
    return combinations(n, m) * p ** m * (1 - p) ** (n - m)


def phi(x):
    return 1 / sqrt(2 * pi) * exp(-x ** 2 / 2)


def x0(n, p, m):
    return (m - n * p) / sqrt(n * p * (1 - p))


def ML_local_theorem(func, n, p):
    return func / (sqrt(n * p * (1 - p)))


def bernoulli_exersice():
    p = float(input("Введите p: "))
    if not (0 <= p <= 1):
        return print("Значение не принадлежит диапазону [0;1]")
    n = int(input("Введите n: "))
    if n < 0:
        print("n не может быть меньше 0")
    m = int(input("Введите m: "))
    if n < m or m < 0:
        print("m не может быть больше")
    m1 = int(input("Введите m1: "))
    if m1 < 0:
        print("m1 не может быть меньше 0")
    m2 = int(input("Введите m2: "))
    if m2 < m1:
        print("m2 не может быть меньше m1")
    print(f"Pn(k == m) = C(n, m) * p^m * q^(n - m) = P{n}({m}) = C({n}, {m}) * {p}^{m} * {1 - p}^({n - m}) = {bernoulli(p, n, m)}")
    print(f"Pn(k >= m) = Σ(i = m, n)Pn(i) = {sum([bernoulli(p, n, i) for i in range(m, n + 1)])}")
    print(f"Pn(k < m) = 1 - Pn(k >= m) = {1 - sum([bernoulli(p, n, i) for i in range(m, n + 1)])}")
    print(f"Pn(m1 <= k <= m2) = Σ(i = m1, m2)Pn(i) = {sum([bernoulli(p, n, i) for i in range(m1, m2 + 1)])}")


def polynomial():
    n = int(input("Введите n: "))
    if n < 1:
        print("n не может быть меньше 1")
    m_arr = []
    k = int(input("Введите k: "))
    if k < 1:
        return print("k не может быть меньше 1")
    for i in range(1, k + 1):
        m = int(input(f"Введите m{i}: "))
        if m < 0:
            return print("m не может быть меньше нуля")
        m_arr.append(m)
    if sum(m_arr) != n:
        return print("Сумма m не равна n")
    p_arr = []
    for i in range(1, k + 1):
        p = float(input(f"Введите p{i}: "))
        if not (0 <= p <= 1):
            return print("Значение не принадлежит диапазону [0;1]")
        p_arr.append(p)
    if not (0.99 <= sum(p_arr) <= 1):
        return print("Сумма вероятностей не равна 1")
    P = factorial(n) / prod([factorial(i) for i in m_arr]) * prod(p_arr[i] ** m_arr[i] for i in range(k))
    print(f"Pn(m1, m2, ..., mk) = n!/(m1! * m2! * ... * mk!) * p1 ^ m1 * p2 ^ m2 * ... * pk ^ mk = {P}")


def exercise1():
    formula = int(input("Выберите формулу:\n1. Бернулли\n2. Полиномиальная\n"))
    if formula == 1:
        return bernoulli_exersice()
    if formula == 2:
        return polynomial()
    return print("Формулы с таким номером нет")


def exercise2():
    n = int(input("Введите n: "))
    if n < 1:
        return print("n не может быть меньше 1")
    p = float(input("Введите p: "))
    if not (0 <= p <= 1):
        return print("Значение не принадлежит диапазону [0;1]")
    m = int(input("Введите m: "))
    if not (0 <= m <= n):
        return print("m не может быть меньше 0 или больше n")
    print("Pn(m) ≈ φ(x0) / sqrt(n * p * q)")
    print("x0 = (m - n * p) / sqrt(n * p * q)")
    print("φ(x) = 1 / sqrt(2 * π) * exp(-x^2 / 2)")
    print(f"Pn(m) ≈ {ML_local_theorem(phi(x0(n, p, m)), n, p)}")


def main():
    n = int(input("Выберите номер задания:\n1. Применение формулы Бернулли и полиномиальной формулы."
          "\n2. Изучение предельных теорем в схеме Бернулли\n"))
    if n == 1:
        return exercise1()
    if n == 2:
        return exercise2()
    print("Нет такого задания")
    return


if __name__ == "__main__":
    main()