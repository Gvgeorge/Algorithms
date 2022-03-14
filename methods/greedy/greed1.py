'''
Задача на программирование: покрыть отрезки точками
По данным n отрезкам необходимо найти множество точек минимального размера,
для которого каждый из отрезков содержит хотя бы одну из точек.
В первой строке дано число 1 ≤ n ≤ 100 отрезков. Каждая из последующих n строк
содержит по два числа 0 ≤ l≤ r ≤ 10**9, задающих начало и конец отрезка.
Выведите оптимальное число m точек и сами m точек.
Если таких множеств точек несколько, выведите любое из них.
Sample Input 1:

3
1 3
2 5
3 6
Sample Output 1:

1
3
Sample Input 2:

4
4 7
1 3
2 5
5 6
Sample Output 2:

2
3 6
'''


import sys
from typing import Iterable


def stepik_runner(func: callable) -> None:
    '''
    Reads input from stdin runs it through func
    and return the result to stdout in the
    stepik console
    '''
    reader = [tuple(map(int, line.split())) for line in sys.stdin]
    lines = reader[1:]
    print(func(lines)[0])
    print(' '.join([str(i) for i in func(lines)[1]]))


def intervals_covered_with_points(lines: Iterable) -> tuple:
    '''
    Greedy algorithm to cover given set of intervals with the
    minimum amount of points
    We sort the intervals by their right ends,
    Then we take the interval with the leftmost right end, add its
    right end to the result, remove the intervals that cross it
    from the set and solve the problem again with remaining intervals.
    '''
    lines = sorted(lines, key=lambda x: x[1])
    result = []
    while lines:
        if not result:
            result.append(lines.pop(0))
        if lines[0][0] <= result[-1][1]:
            del lines[0]
        else:
            result.append(lines.pop(0))
    result = [line[1] for line in result]
    return (len(result), result)


stepik_runner(intervals_covered_with_points)
