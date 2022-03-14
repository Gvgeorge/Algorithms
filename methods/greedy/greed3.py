'''
По данному числу 1 ≤ n ≤ 10**9  найдите максимальное число k,
для которого n можно представить как сумму k различных натуральных слагаемых.
Выведите в первой строке число k, во второй — k слагаемых.
Числа не могут повторяться
Sample Input 1:

4
Sample Output 1:

2
1 3
Sample Input 2:

6
Sample Output 2:

3
1 2 3
'''


import sys


def stepik_runner(func: callable) -> None:
    '''
    Reads input from stdin runs it through func
    and return the result to stdout in the
    stepik console
    '''
    input_number = int(sys.stdin.read())
    result = func(input_number)
    print(len(result))
    print(' '.join([str(numb) for numb in result]))


def list_of_numbers(number: int) -> list[int]:
    '''
    Greedy alg that for the given input number
    returns the maximum possible list of unique natural
    numbers sum of which equals to the input number

    >>>list_of_numbers(12)
    >>>[1, 2, 3, 6]
    '''
    if number <= 1:
        return [number]

    result = []
    summ = 0
    for n in range(1, number):
        if summ + 2 * n + 1 > number:
            result.append(number - summ)
            break
        result.append(n)
        summ += n
    return result


stepik_runner(list_of_numbers)
