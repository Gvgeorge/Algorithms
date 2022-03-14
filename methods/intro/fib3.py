'''
Даны целые числа 1 ≤n≤ 10**18 и 2 ≤ m ≤ 10**5,
необходимо найти остаток от деления n-го числа Фибоначчи на m.
Sample Input:

10 2
Sample Output:

1
'''


def fib_last(n: int) -> int:
    '''
    Calculates n-th fib number
    '''
    if n <= 1:
        return n
    fib_1, fib_2 = 0, 1
    for idx in range(2, n + 1):
        fib_1, fib_2 = fib_2, fib_1 + fib_2
    return fib_2


def pisano_period(m: int) -> int:
    '''
    Calculates length of the pisano period for the number - m
    '''
    previous, current = 0, 1
    for i in range(0, m ** 2 + 1):
        previous, current = current, (previous + current) % m
        if (previous == 0 and current == 1):
            return i + 1


def fib_mod(n: int, m: int) -> int:
    '''
    Calculates the last digit of n-th fib number
    using pisano period
    '''
    pisano = pisano_period(m)
    return fib_last(n % pisano) % m


def main():
    n, m = map(int, input().split())
    print(fib_mod(n, m))


if __name__ == "__main__":
    main()
