
'''
В первой строке даны целое число 1≤n≤10**5 и массив A[1…n] из n различных
натуральных чисел, не превышающих 10^9, в порядке возрастания, во второй —
целое число 1 ≤ k ≤ 10**5 и k натуральных чисел b1....,bk, не превышающих 10^9.
Для каждого i от 1 до k необходимо вывести индекс 1 ≤ j ≤ n, для которого
A[j]=bi или -1, если такого j нет.
Sample Input:

5 1 5 8 12 13
5 8 1 23 1 11

Sample Output:

3 1 -1 1 -1
'''


import sys


def bsearch(value: int, lst: list) -> int:
    '''
    Bisectional search implementation
    returns -1 if value isn't found
    '''
    if not lst:
        return -1

    left = 0
    right = len(lst) - 1

    while left <= right:
        middle = (left + right)//2
        if lst[middle] == value:
            return middle
        elif lst[middle] < value:
            left = middle + 1
        else:
            right = middle - 1
    return -1


first_line = [int(x) for x in sys.stdin.readline().strip().split()][1:]
second_line = [int(x) for x in sys.stdin.readline().strip().split()][1:]
result = [str(bsearch(x, first_line) + 1)
          if bsearch(x, first_line) >= 0 else '-1' for x in second_line]

print(' '.join(result))
