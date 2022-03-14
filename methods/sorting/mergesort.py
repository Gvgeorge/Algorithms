'''
Первая строка содержит число 1 ≤ n ≤10**5, вторая — массив A[1…n], содержащий
натуральные числа, не превосходящие 10^9. Необходимо посчитать число пар
индексов 1 ≤ i < j ≤n, A[i]>A[j]. (Такая пара элементов называется инверсией
массива. Количество инверсий в массиве является в некотором смысле его мерой
неупорядоченности: например, в упорядоченном по неубыванию массиве инверсий
нет вообще, а в массиве, упорядоченном по убыванию, инверсию образуют
каждые два элемента.)

Sample Input:
5
2 3 9 2 9
Sample Output:
2
'''

import sys


class MergeSorter:
    def __init__(self):
        self._counter = 0

    def reset_counter(self):
        self._counter = 0

    def get_counter(self) -> int:
        return self._counter

    def merge(self, left: list, right: list) -> list:
        left_idx = 0
        right_idx = 0
        left_len = len(left)
        right_len = len(right)
        result = []
        while left_idx < left_len and right_idx < right_len:

            if left[left_idx] <= right[right_idx]:
                result.append(left[left_idx])
                left_idx += 1
            else:
                result.append(right[right_idx])
                right_idx += 1

                self.counter += left_len - left_idx

        if left_idx == left_len:
            while right_idx < right_len:
                result.append(right[right_idx])
                right_idx += 1

        elif right_idx == right_len:
            while left_idx < left_len:
                result.append(left[left_idx])
                left_idx += 1

        return result

    def merge_sort(self, lst: list) -> list:
        length = len(lst)
        if length <= 1:
            return lst
        mid = length // 2
        left = self.merge_sort(lst[:mid])
        right = self.merge_sort(lst[mid:])
        return self.merge(left, right)


first_line = sys.stdin.readline()
second_line = [int(x) for x in sys.stdin.readline().strip().split()]
merge_sorter = MergeSorter()
merge_sorter.merge_sort(second_line)
print(merge_sorter.get_counter())
