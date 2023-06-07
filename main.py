from math import factorial


def soc(n, m):  # Функция для формулы выбора без возврата и без упорядочивания
    c = (factorial(n)) / (factorial(m) * factorial(n - m))
    return c


def scheme1(i):
    qI = [0] * i
    for j in range(0, i):
        qI[j] = float(input("Введите вероятность отказа " + str(j + 1) + "-го элемента: "))

    p = (qI[0] + qI[3] - (qI[0] * qI[3])) * qI[2] * (qI[1] + qI[4] - (qI[1] * qI[4]))
    print("(P(q1) + P(q4) - P(q1 q4)) * P(q3) * (P(q2) + P(q5) - P(q2 q5)) = " + str(round(p, 5)))


def fullProbability(n, choose):
    hI = [0] * n
    hAI = [0] * n
    p = 0
    err = 0
    for i in range(0, n):
        hI[i] = float(input("введите вероятность события P(H" + str(i + 1) + "): "))
    for u in range(0, n):
        err += hI[u]

    if err == 1:
        for t in range(0, n):
            hAI[t] = float(input("введите вероятность события P(H" + str(t + 1) + "|A): "))
            p += hAI[t] * hI[t]
        print("P(A) = " + str(round(p, 5)))
        ch = str(input("Желаете решить по формуле Байеса? "))
        if ch == "yes":
            while ch == "yes":
                b = int(input("Какое из событий H принять за благоприятсвующее?: "))
                answ = (hI[b - 1] * hAI[b - 1]) / p
                print("P(A|H" + str(b) + ") = " + str(round(answ, 5)))
                ch = str(input("Желаете выбрать другое событие? "))
    else:
        print("Error: Сумма полной группы событий не равна 1!")


def ptickets(n, m1, m2, k, t, t1):
    Astudent = (soc(m1, t) * soc(n - m1, k - t)) / soc(n, k)
    Bstudent = (soc(m2, t) * soc(n - m2, k - t)) / soc(n, k)
    for i in range((t + 1), (t1 + 1)):
        next1 = (soc(m1, i) * soc(n - m1, k - i)) / (soc(n, k))
        next2 = (soc(m2, i) * soc(n - m2, k - i)) / (soc(n, k));
        Astudent += next1
        Bstudent += next2

    print("1-Найти вероятность того,что только первый студент ответит правильно")
    print("2-Найти вероятность того,что только второй студент ответит правильно")
    print("3-Найти вероятность того,что оба студента ответят правильно")
    print("4-Найти вероятность того,что оба студента не ответят правильно ни на 1 вопрос")
    print("5-Найти вероятность того,что только 1 из них ответит правильно")
    print("6-Найти вероятность того,что хотя бы 1 из них ответит правильно")
    slychai = int(input("Выберите задачу :"))
    if slychai == 1:
        Astudent *= (1 - Bstudent)
        return Astudent
    elif slychai == 2:
        Bstudent *= (1 - Astudent)
        return Bstudent
    elif slychai == 3:
        sumTWOstudent = Astudent * Bstudent
        return sumTWOstudent
    elif slychai == 4:
        sumTWOstudentNot = 1 - (Astudent * Bstudent)
        return sumTWOstudentNot
    elif slychai == 5:
        OnlyOne = (Astudent * (1 - Bstudent)) + (Bstudent * (1 - Astudent))
        return OnlyOne
    elif slychai == 6:
        AtLeastOne = (Astudent * (1 - Bstudent)) + (Bstudent * (1 - Astudent)) + (Astudent * Bstudent)
        return AtLeastOne
    else:
        print("Данной задачи не существует.\n Пожалуйста, повторите попытку и убедитесь в правильности ввода")
        return -1


def errorPrint(n, m1, m2, k, t, t1):
    if ((m1 > n or m1 < 0) or (m2 > n or m2 < 0)
            or (k >= n or k < 0) or (t < 0 or t > k) or (t1 > k or t1 < 0)
            or (t > t1) or (n < 0)):
        if ((m1 < 0) or (m2 < 0) or (k < 0) or (t < 0) or (t1 < 0) or (n < 0)):
            print("Какое-то или какие-то данные отрицательны!")
        if (m1 > n):
            print("m1>n")
        if (m2 > n):
            print("m2>n")
        if (k > n):
            print("k>n")
        if (t > k):
            print("t>k")
        if (t1 > k):
            print("t1>k")
        if (t > t1):
            print("t>t1")
        return 0
    else:
        return 1


print(
    "выберите одну из 4-x задач: \n1) Электрическая цепь состоит из пяти элементов составлена по схеме, приведённой на рисунке.\nНайти вероятность разрыва цепи, предполагая, что отказы отдельных элементов независимы и равны.")
print(
    "2) Один студент выучил m1 из n опросов программы, а второй m2. Каждому из них задают по t вопросов. Найти вероятность того, что не менее, чем на два вопроса ответят...")
print("3) Решение с помощью формул полной вероятности и Байеса")
choose = int(input())

if (choose == 3):
    n = int(input("введите количество событий: "))
    fullProbability(n, choose)
elif (choose == 1):
    scheme1(5)
elif choose == 2:
    sum = 0
    n = 0
    n = int(input("Введите общее кол-во билетов n="))
    m1 = int(input("Введите кол-во билетов выученных первым студентом m1="))
    m2 = int(input("Введите кол-во билетов выученных вторым студентом m2="))
    k = int(input("Введите кол-во билетов,которые спрашивают у студентов k="))
    t = int(input(
        "Введите предел кол-ва билетов, на который должны ответить студенты в виде ( от 1 до 3 (не менее 1) ,\nесли хотите чтобы отвечали только на t попросов,то вводите от 1 до 1 от t="))
    t1 = int(input("до t1 = "))
    flag = True
    while flag:
        if (errorPrint(n, m1, m2, k, t, t1) == 1):
            sum = ptickets(n, m1, m2, k, t, t1)
            if (sum != -1):
                print("Итоговая вероятность равна " + str(sum))
        p = int(input(
            "Введите любое число если хотите посмотреть ответы на другие задачи или любой другой символ (отличный от числа) для завершения программы"))
        if (p == 0): flag = False
