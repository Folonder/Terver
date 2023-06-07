from math import factorial


def combinations(n, k):
    return factorial(n) / (factorial(n - k) * factorial(k))


def exercise1():
    elems = []
    for i in range(1, 6):
        print(f"Введите вероятность отказа {i}-го элемента:", end=" ")
        elem = float(input())
        if not (0 <= elem <= 1):
            print("Веротяность должна быть в диапазоне 0 <= P <= 1")
            return
        elems.append(elem)
    p = (elems[0] + elems[3] - (elems[0] * elems[3])) * elems[2] * (elems[1] + elems[4] - (elems[1] * elems[4]))
    print(f"(P(A1) + P(A4) - P(A1 A4)) * P(A3) * (P(A2) + P(A5) - P(A2 A5)) = {round(p, 5)}")


def exercise2():
    elems = []
    for i in range(1, 7):
        print(f"Введите вероятность отказа {i}-го элемента:")
        elem = int(input())
        if not (0 <= elem <= 1):
            print("Веротяность должна быть в диапазоне 0 <= P <= 1")
            return
        elems.append(elem)
    p = elems[5] + elems[2] * (elems[0] + elems[3] - elems[0] * elems[3]) * (elems[1] + elems[4] - elems[1] * elems[4])
    print(f"P(A6) + P(A3) * (P(A1) + P(A4) - P(A1) * P(A4)) * (P(A2) + P(A5) - P(A2) * P(A5))")


def exercise3():
    n = int(input("Введите n:\n"))
    m1 = int(input("Введите m1:\n"))
    m2 = int(input("Введите m2:\n"))
    if m1 > n or m2 > n:
        print("Число выученных вопросов не может быть больше числа вопросов")
        return
    print("A1 - первый студент, ответил не менее, чем на два вопроса правильно.")
    print("A2 - второй студент, ответил не менее, чем на два вопроса правильно.")
    A1 = (combinations(m1, 3) + combinations(m1, 2) * combinations(n - m1, 1)) / combinations(n, 3)
    A2 = (combinations(m2, 3) + combinations(m2, 2) * combinations(n - m2, 1)) / combinations(n, 3)
    print(f"P(A1) = (C(m1, 3) + C(m1, 2) * C(n - m1, 1)) / C(n, 3) = {A1}")
    print(f"P(A1) = (C(m2, 3) + C(m2, 2) * C(n - m2, 1)) / C(n, 3) = {A2}")
    print("A - оба студента ответят")
    print(f"P(A) = P(A1) * P(A2) = {A1 * A2}")
    print("B - ответит только первый студент")
    print(f"P(B) = P(A1) * P(!A2) = {A1 * (1 - A2)}")
    print("C - ответит только один из них:")
    print(f"P(C) = P(A1) * P(!A2) + P(A2)*P(!A1) = {A1 * (1 - A2) + A2 * (1 - A1)}")
    print(f"D - ответят на вопросы хотя бы один из них")
    print(f"P(N) = P(A1) + P(A2) - P(A1) * P(A2) = {A1 + A2 - A1 * A2}")


def exercise4():
    print("Введите число событий")
    amount = int(input())
    events = []
    if amount <= 0:
        print("Число событий не может быть меньше 1")
        return
    for i in range(1, amount + 1):
        event = float(input(f"Введите вероятность {i} события: "))
        if event < 0:
            print("Вероятность события не может быть меньше 0")
            return
        events.append(event)
    if round(sum(events), 2) < 0.99:
        print("Суммая вероятностей меньше 1")
    probabilities = []
    for i in range(1, amount + 1):
        probability = float(input(f"Введите условную вероятность события {i}: "))
        if probability < 0:
            print("Условная вероятность не может быть меньше 0")
            return
        probabilities.append(probability)
    full_probability = sum([p[0] * p[1] for p in zip(events, probabilities)])
    print(f"P(A) = {' + '.join([f'P(H{i}) * P(A/H{i})' for i in range(1, amount + 1)])} = {full_probability}")
    for event_num in range(1, amount + 1):
        print(f"P(H{event_num}|A) = P(H{event_num}) * P(A|H{event_num}) / P(A) = {events[event_num - 1] * probabilities[event_num - 1] / full_probability}")


def main():
    print("Выберите номер задачи:\nЗадание 1.Нахождение вероятности безотказной работы заданной схемы"
          " (или отказа схемы), используя алгебраические операции над событиями и теоремы сложения и"
          " умножения вероятностей.\nЗадание 2.Модифицированная схема из 1 задания.\nЗадание 3. Один студент выучил m1 из n вопросов программы,"
          " а второй m2. Каждому из них задают по три вопроса. Найти вероятность того, что не менее, чем на два "
          "вопроса правильно ответят:\nЗадание 4. Задача на полную вероятность или Байеса")
    exercise = int(input())
    if exercise == 1:
        exercise1()
    elif exercise == 2:
        exercise2()
    elif exercise == 3:
        exercise3()
    elif exercise == 4:
        exercise4()
    else:
        print("Такого задания нет")


if __name__ == "__main__":
    main()