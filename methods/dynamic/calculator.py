'''
У вас есть примитивный калькулятор, который умеет выполнять всего три операции
с текущим числом x: заменить x на 2x, 3x или x+1. По данному целому числу
1 ≤ n ≤10**5  определите минимальное число операций k, необходимое, чтобы
получить n из 1. Выведите k и последовательность промежуточных чисел.

Sample Input 1:
1
Sample Output 1:
0
1

Sample Input 2:
5
Sample Output 2:
3
1 2 4 5

Sample Input 3:
96234
Sample Output 3:
14
1 3 9 10 11 22 66 198 594 1782 5346 16038 16039 32078 96234
'''


import sys


class DivCalcNode:
    def __init__(self, value: int):
        self.value = value
        self.minus_one = None
        self.div_by_two = None
        self.div_by_three = None
        self.parent = None

    def generate_children(self) -> None:
        if self.value % 3 == 0:
            self.div_by_three = DivCalcNode(self.value/3)
            self.div_by_three.parent = self
        if self.value % 2 == 0:
            self.div_by_two = DivCalcNode(self.value/2)
            self.div_by_two.parent = self
        if self.value > 1:
            self.minus_one = DivCalcNode(self.value - 1)
            self.minus_one.parent = self

    @property
    def depth(self) -> int:
        '''
        calculates the depth (height) of a subtree of a given node
        '''
        if not self.parent:
            return 1
        return 1 + self.parent.depth

    @property
    def children(self) -> list:
        return [self.div_by_three, self.div_by_two, self.minus_one]

    def __str__(self):
        return f'DivCalcNode of value {self.value}'


def calculator(node, result=None) -> DivCalcNode:
    '''
    builds a tree
    returns a leaf node of the most optimal sequence
    '''
    if node.value == 1:
        return node
    node.generate_children()
    for child in node.children:
        if child is None:
            continue
        if result is None:
            if child.value == 1:
                result = child
        else:
            if child.depth >= result.depth:
                break
            if child.depth < result.depth and child.value == 1:
                result = child
                break
        result = calculator(child, result)
    return result


def number_sequence(node: DivCalcNode) -> list:
    '''
    Goes up the tree from a leaf and pushes every node
    on its way to the list
    '''
    seq = []
    while node.parent:
        seq.append(node.value)
        node = node.parent
    return seq


input = int(sys.stdin.readline())
result_node = calculator(DivCalcNode(input))
print(result_node.depth - 1)
result_sequence = [int(number) for number in number_sequence(result_node)]
result_sequence.append(input)
print(' '.join([str(number) for number in result_sequence]))
