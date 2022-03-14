'''
В первой строке задано два целых числа 1 ≤ n ≤ 50000 и 1 ≤ m ≤ 50000 —
количество отрезков и точек на прямой, соответственно. Следующие n строк
содержат по два целых числа ai и bi (ai <= bi) — координаты концов отрезков.
Последняя строка содержит mm целых чисел — координаты точек. Все координаты
не превышают 10^8 по модулю. Точка считается принадлежащей отрезку, если она
находится внутри него или на границе. Для каждой точки в порядке появления
во вводе выведите, скольким отрезкам она принадлежит.

Sample Input:

2 3
0 5
7 10
1 6 11
Sample Output:

1 0 0
'''


import random
import sys
import bisect


LOWER_BOUND = 0
UPPER_BOUND = 1


def quick_sort(lst: list, left: int, right: int, tuple_idx: int) -> None:
    '''
    Quick sort algorithm for lists containing two element tuples.
    Pivot points are chosen randomly.
    lst - list to be sorted
    left - left bound of the slice
    right - right bound of the slice
    tuple_idx = the index by which sorting will take place
    '''
    while left < right:
        random_idx = random.randrange(left, right)
        lst[left], lst[random_idx] = lst[random_idx], lst[left]

        left_pivot, right_pivot = partition(lst, left, right, tuple_idx)
        if left < left_pivot:
            quick_sort(lst, left, left_pivot, tuple_idx)
        left = right_pivot


def partition(lst: list, left: int, right: int, tuple_idx: int) -> tuple:
    '''
    lst - list to be sorted
    left - left bound of the slice
    right - right bound of the slice
    tuple_idx = the index by which sorting will take place

    should be called with quicksort function implements the actual
    sorting mechanism of the quicksort alg
    takes into account situations when there are many
    duplicate items in the list. The returned tuple contains two
    boundaries for the slice with duplicates.
    '''
    pivot = left
    split_idx = left + 1
    eq_idx = 0

    for i in range(left + 1, right+1):
        if lst[i][tuple_idx] <= lst[pivot][tuple_idx]:
            lst[i], lst[split_idx] = lst[split_idx], lst[i]
            split_idx += 1

    lst[split_idx-1], lst[pivot] = lst[pivot], lst[split_idx-1]

    for i in range(split_idx - 2, left-1, -1):
        if lst[i][tuple_idx] == lst[split_idx - 1][tuple_idx]:
            eq_idx += 1
            lst[i], lst[split_idx - 1 - eq_idx] = \
                lst[split_idx - 1 - eq_idx], lst[i]

    return split_idx - 1 - eq_idx, split_idx


ranges_num, _ = sys.stdin.readline().strip().split()
ranges = []
lower_bounds = []
upper_bounds = []
for idx in range(int(ranges_num)):
    range_ = [int(x) for x in sys.stdin.readline().strip().split()]
    ranges.append(range_)

dots = [int(x) for x in sys.stdin.readline().strip().split()]

quick_sort(ranges, 0, len(ranges)-1, LOWER_BOUND)
lower_bounds = [x[0] for x in ranges]
quick_sort(ranges, 0, len(ranges)-1, UPPER_BOUND)
upper_bounds = [x[1] for x in ranges]


def get_number_of_ranges_for_dot(dot: tuple) -> int:
    b_left = bisect.bisect_right(lower_bounds, dot)
    b_right = bisect.bisect_left(upper_bounds, dot)
    return b_left - b_right


res = []
for dot in dots:
    res.append(get_number_of_ranges_for_dot(dot))
print(' '.join([str(x) for x in res]))
