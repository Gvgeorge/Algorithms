'''
Вычислите расстояние редактирования двух данных непустых строк длины
не более 10^2, содержащих строчные буквы латинского алфавита.

Sample Input 1:
ab
ab

Sample Output 1:
0

Sample Input 2:
short
ports

Sample Output 2:
3
'''

from functools import lru_cache
import sys


string_a = sys.stdin.readline()
string_b = sys.stdin.readline()


def diff(string_a: str, string_b: str) -> int:
    '''
    compares last two chars of a given string
    '''
    return 0 if string_a[-1] == string_b[-1] else 1


def edi_distance(string_a: str, string_b: str) -> int:
    '''
    recursively calculates editing distance
    '''
    @lru_cache(maxsize=None)
    def comp(string_a: str, string_b: str) -> int:
        if len(string_a) == 0:
            return len(string_b)
        elif len(string_b) == 0:
            return len(string_a)
        else:
            return min(
                comp(string_a, string_b[:-1]) + 1,
                comp(string_a[:-1], string_b) + 1,
                comp(string_a[:-1], string_b[:-1]) + diff(string_a, string_b)
                       )
    return comp(string_a, string_b)


def edi_distance_iter(string_a, string_b):
    '''
    iteratively calculates editing distance
    '''

    len_a, len_b = len(string_a), len(string_b)
    value_list = [[0]*(len_b+1) for i in range(len_a+1)]

    for i in range(len_b+1):
        value_list[0][i] = i

    for j in range(len_a+1):
        value_list[j][0] = j

    for a in range(1, len_a + 1):
        for b in range(1, len_b+1):
            value_list[a][b] = min(
                value_list[a-1][b] + 1,
                value_list[a][b-1] + 1,
                value_list[a-1][b-1] + diff(string_a[a-1], string_b[b-1])
                        )
    return value_list[-1][-1]


print(edi_distance_iter(string_a, string_b))
