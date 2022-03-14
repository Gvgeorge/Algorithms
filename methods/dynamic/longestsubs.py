'''
Дано целое число 1 ≤ n ≤ 10**3 и массив A[1…n] натуральных чисел,
не превосходящих 2⋅10**9. Выведите максимальное 1 ≤ k ≤ n, для
которого найдётся подпоследовательность 1 ≤ i1 < i2 < … < ik ≤ n длины k,
в которой каждый элемент делится на предыдущий.

Sample Input:

4
3 6 7 12
Sample Output:

3
'''

import sys

length = sys.stdin.readline()
input = [int(i) for i in sys.stdin.readline().split()]


def LIS_bottom_up_divisibility(array: list) -> int:
    val_array = [1 for i in range(len(array))]

    for i in range(len(val_array)):
        for j in range(i):
            if array[i] % array[j] == 0 and val_array[i] < val_array[j] + 1:
                val_array[i] = val_array[j] + 1

    return max(val_array)


print(LIS_bottom_up_divisibility(input))
