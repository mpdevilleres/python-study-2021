# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
# for a given fibonacci sequence
# find the nth number (7)
# find the sum of all number up to nth number

# 100 - 120

def fibonacci(n):
    a = 0
    b = 1
    nth = 0

    if n == 1:
        return a
    elif n == 2:
        return b

    for i in range(n - 2):
        nth = a + b
        a = b
        b = nth

    return nth


def exercise(n):
    t = 0
    for i in range(n + 1):
        t += fibonacci(i)

    f = fibonacci(n)
    print(f'{f:,}')
    print(f'{t:,}')


exercise(200)
