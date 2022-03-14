'''
Первая строка содержит количество предметов 1 ≤ n ≤ 10**3
и вместимость рюкзака 0 ≤ W ≤ 2⋅10**6.
Каждая из следующих nn строк задаёт стоимость 0 ≤ ci ≤ 2⋅10**6
и объём 0 ≤ wi ≤ 2⋅10**6 предмета (n, W, ci, wi — целые числа).
Выведите максимальную стоимость частей предметов
(от каждого предмета можно отделить любую часть, стоимость и
объём при этом пропорционально уменьшатся), помещающихся в
данный рюкзак, с точностью не менее трёх знаков после запятой.
Sample Input:

3 50
60 20
100 50
120 30
Sample Output:

180.000
'''


import sys


def stepik_runner(func: callable) -> None:
    '''
    Reads input from stdin runs it through func
    and return the result to stdout in the
    stepik console
    '''
    reader = [tuple(map(int, line.split())) for line in sys.stdin]
    print(reader)
    volume = reader[0][1]
    items = reader[1:]
    print('{:.3f}'.format(func(items, volume)))


def knapsack(items: list[tuple[int, int]], max_volume: int) -> float:
    '''
    Greedy algortithm for solving knapsack problem, items variable
    consists of items [price, weight], taking parts of items is allowed
    '''
    items = sorted(items, key=lambda x: x[0]/x[1])
    total_cost = 0
    current_volume = 0
    while current_volume < max_volume:
        if not items:
            break
        most_expensive_item = items.pop()
        volume_left = max_volume - current_volume
        if volume_left >= most_expensive_item[1]:
            total_cost += most_expensive_item[0]
            current_volume += most_expensive_item[1]
        else:
            total_cost += volume_left/most_expensive_item[1] * \
                most_expensive_item[0]
            current_volume += volume_left
    return float(total_cost)


stepik_runner(knapsack)
