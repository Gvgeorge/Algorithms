'''
Первая строка входа содержит целые числа 1 ≤ W ≤ 10**4  и
1 ≤ n ≤ 300 — вместимость рюкзака и число золотых слитков. Следующая
строка содержит n целых чисел 0 ≤ w1,…,wn ≤ 10**5, задающих веса
слитков. Найдите максимальный вес золота, который можно унести в рюкзаке.
Sample Input:
10 3
1 4 8

Sample Output:

9
'''

import bisect
import sys


size, n_items = sys.stdin.readline().split()
items = [int(i) for i in sys.stdin.readline().split()]
size = int(size)


def knapsack(size: int, items: list) -> int:
    items.sort()
    items = items[:bisect.bisect_right(items, size)]
    n_items = len(items)
    value_table = [[0]*(size+1) for item in range(n_items+1)]
    for i in range(1, n_items+1):
        item_row = value_table[i]
        for j in range(size+1):
            if j >= items[i-1] + value_table[i-1][j-items[i-1]]:
                item_row[j] = max(items[i-1] + value_table[i-1][j-items[i-1]],
                                  value_table[i-1][j])
            elif j >= items[i-1]:
                item_row[j] = items[i-1]
            else:
                item_row[j] = value_table[i-1][j]
    print(value_table)
    return value_table[-1][-1]


print(knapsack(size, items))
