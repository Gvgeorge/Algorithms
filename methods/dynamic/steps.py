'''
Даны число 1 ≤ n ≤ 10^2 ступенек лестницы и целые числа −10**4 ≤a1,…,an ≤10**4,
которыми помечены ступеньки. Найдите максимальную сумму, которую можно получить
идя по лестнице снизу вверх (от нулевой до n-й ступеньки), каждый раз
поднимаясь на одну или две ступеньки.

Sample Input 1:
2
1 2
Sample Output 1:
3

Sample Input 2:
2
2 -1
Sample Output 2:
1

Sample Input 3:
3
-1 2 1
Sample Output 3:
3
'''


import sys
from functools import lru_cache


num_steps = int(sys.stdin.readline())
step_marks = [int(i) for i in sys.stdin.readline().split()]


class Tree:
    '''This tree is defined by its root'''
    def __init__(self, value: int,
                 left: 'Tree' = None, right: 'Tree' = None):
        self.parent = None
        self.value = value
        self.left = left
        self.right = right

    def set_left(self, other: 'Tree'):
        self.left = other

    def set_right(self, other: 'Tree'):
        self.right = other

    @property
    def leaves(self) -> list:
        '''
        Returns a list with all the leaves of the tree
        '''
        current_nodes = [self]
        leaves = []

        while len(current_nodes) > 0:
            next_nodes = []
            for node in current_nodes:
                if node.left is None and node.right is None:
                    leaves.append(node)
                    continue
                if node.left is not None:
                    next_nodes.append(node.left)
                if node.right is not None:
                    next_nodes.append(node.right)
            current_nodes = next_nodes
        return leaves

    def __str__(self):
        return f'Tree with root with value {self.value}'

    def __repr__(self):
        return f'Tree with root with value {self.value}'


def tree_ladder(step_marks: list) -> Tree:
    '''
    builds a tree with all possible steps
    '''
    step_marks = [0] + list(step_marks)
    node_list = [Tree(i) for i in step_marks]
    for step, cur_node in enumerate(node_list):
        try:
            cur_node.set_left(node_list[step+1])
        except IndexError:
            pass
        try:
            cur_node.set_right(node_list[step+2])
        except IndexError:
            pass
    return node_list[0]


@lru_cache(maxsize=None)
def recurse_tree(root: Tree):
    '''
    calculates max_value of a given tree
    '''
    if (not root.left) and (not root.right):
        return root.value
    elif not root.left:
        return root.value + recurse_tree(root.right)
    elif not root.right:
        return root.value + recurse_tree(root.left)
    return max(root.value + recurse_tree(root.left),
               root.value + recurse_tree(root.right))


print(recurse_tree(tree_ladder(step_marks)))
