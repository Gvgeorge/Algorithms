'''
Первая строка содержит число  1≤n≤10**4, вторая — nn натуральных чисел,
не превышающих 10. Выведите упорядоченную по неубыванию последовательность
этих чисел.
Sample Input:
5
2 3 9 2 9

Sample Output:
2 2 3 9 9
'''
import sys

sys.stdin.readline()
initial_list = [int(x) for x in sys.stdin.readline().split()]


def count_sort(lst: list) -> list:
    '''
    функция для сортировки подсчетом
    '''
    highest_number = max(lst)
    # инициализируем список в котором будем сохранять количество повторений
    # каждого числа (длины максимального числа начального списка)
    # и результирующий список (длины такой же как у начального листа)
    count_list = [0 for i in range(highest_number)]
    res_list = [0 for i in range(len(lst))]
    # заполняем count_list количеством повторений чисел в начальном листе
    for i in lst:
        count_list[i-1] += 1
    # считаем куммулятивные суммы
    for i in range(1, len(count_list)):
        count_list[i] += count_list[i-1]

    # заполняем результирующий лист
    for i in range(len(lst)-1, -1, -1):
        res_list[count_list[lst[i]-1]-1] = lst[i]
        count_list[lst[i]-1] -= 1

    return [str(i) for i in res_list]


print(' '.join(count_sort(initial_list)))
