'''
Дано целое число 1 ≤ n ≤ 10**5 A[1…n], содержащий неотрицательные целые числа,
не превосходящие 10^9. Найдите наибольшую невозрастающую
подпоследовательность в A.
В первой строке выведите её длину k, во второй — её индексы.
Sample Input:

5
5 3 4 4 2
Sample Output:

4
1 3 4 5
'''


import sys


length = sys.stdin.readline()
input = [int(i) for i in sys.stdin.readline().split()]


class Card:
    '''
    For easier vizualisation I represent items in the list as cards
    '''
    def __init__(self, idx: int, pointer: 'Card'):
        self.idx = idx
        self.pointer = pointer

    def get_idx(self) -> int:
        return self.idx

    def get_pointer(self) -> 'Card':
        return self.pointer

    def set_idx(self, idx):
        self.idx = idx

    def set_pointer(self, pointer: 'Card'):
        self.pointer = pointer

    def __str__(self):
        if isinstance(self.pointer, Card):
            pointer = self.pointer.get_idx()
        else:
            pointer = self.pointer
        return f'{self.idx} ==> {pointer}'

    def __repr__(self):
        return self.__str__()


def patient_sort(array: list) -> list:
    '''
    We first create a stack list
    Then we go through cards
    if stack list empty we will add add a new stack with current single card
    else:
        find the pos to insert the card within the last cards of the stacks
        using bisectional search
        if pos == 0:
            append the card to the 0th stack and set card's pointer to -1
        if pos == len(stack_list):
            create a new stack with current single card and a pointer to
            the last card of previous stack
        else:
            append the card to the stack in the pos and set pointer to
            the last card of previous stack
    '''
    stack_list = []

    for idx, item in enumerate(array):
        item = array[idx]
        if len(stack_list) == 0:
            stack_list.append([Card(idx, -1)])
            continue
        position = bisect_stacklist(item, array, stack_list)
        if position == 0:
            stack_list[0].append(Card(idx, -1))
        elif position == len(stack_list):
            stack_list.append([Card(idx, stack_list[-1][-1])])
        else:
            stack_list[position].append(Card(idx, stack_list[position-1][-1]))

    lis = []
    card = stack_list[-1][-1]
    while True:
        if card == -1:
            break
        lis.append(card)
        card = card.get_pointer()

    res = []
    for card in lis[::-1]:
        res.append(card.get_idx() + 1)
    return res


def bisect_stacklist(item: Card, array: list, stack_list: list) -> int:
    '''
    find the position to insert a card to the stack_list
    '''
    lower_bound = 0
    upper_bound = len(stack_list)
    while lower_bound < upper_bound:
        mid = (lower_bound + upper_bound)//2
        if item <= array[stack_list[mid][-1].get_idx()]:
            lower_bound = mid + 1
        else:
            upper_bound = mid
    return lower_bound


ans = patient_sort(input)
print(len(ans))
print(' '.join([str(i) for i in ans]))
