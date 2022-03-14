'''
Дано число 1 ≤ n ≤ 10**7,
необходимо найти последнюю цифру n-го числа Фибоначчи.
Sample Input:

841645
Sample Output:

5
'''


def fib_digit(n: int) -> int:
    '''
    Calculates the last digit of n-th fib number
    '''
    if n <= 1:
        return n
    fib_1, fib_2 = 0, 1
    for idx in range(2, n + 1):
        fib_1, fib_2 = fib_2 % 10, (fib_1 + fib_2) % 10
    return fib_2


def main():
    n = int(input())
    print(fib_digit(n))


if __name__ == "__main__":
    main()
