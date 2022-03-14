'''
Дано целое число 1 ≤ n ≤ 40, необходимо вычислить n-е число Фибоначчи
'''


def cached(func: callable) -> callable:
    cache = {}

    def decorator(n: int) -> int:
        if n in cache:
            return cache[n]
        cache[n] = func(n)
        return cache[n]

    return decorator


@cached
def fib(n: int) -> int:
    '''
    Recursive fibonacci algorithm with memoization
    '''
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)


def main():
    n = int(input())
    print(fib(n))


if __name__ == "__main__":
    main()
