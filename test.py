# import random
#
# with open('Lab5/z2_var23.txt') as f:
#     string = '.'.join(f.readline().split(','))
#
# with open('Lab5/z2_var23.txt') as f:
#     print('.'.join(f.readline().split(',')))


with open("big.xml", "w") as f:
    print("<b>", file=f)
    for i in range(500):
        print(f"<a{str(i)}>", file=f)
        for j in range(5000):
            print(f"<a{str(i)}_{str(j)}>", file=f)
        for j in range(4999, -1, -1):
            print(f"</a{str(i)}_{str(j)}>", file=f)
        print(f"</a{str(i)}>", file=f)
    print("</b>", file=f)