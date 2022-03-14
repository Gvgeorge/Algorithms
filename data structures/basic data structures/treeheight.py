import sys


sys.setrecursionlimit(30000)


class Node:
    def __init__(self, value: int):
        self.value = value
        self.children = set()
        self.parent = None
        self._height = 1

    def add_child(self, child: 'Node') -> None:
        self.children.add(child)

    @property
    def list_children(self) -> set:
        return self.children

    def set_parent(self, other: 'Node') -> None:
        self.parent = other
        other.add_child(self)

    def is_leaf(self) -> bool:
        if not self.children:
            return True
        return False

    @property
    def height(self):
        return self._height

    def __str__(self):
        return f'Node of value {self.value}'


class Tree:
    def __init__(self, root: Node):
        self.root = root
        self._leaves = []

    @property
    def leaves(self) -> list:
        return self._leaves

    def get_height(self) -> int:
        '''
        recursively calculates height of the tree
        '''
        if self.root.is_leaf():
            return 1
        temp_height = 0
        for leaf in self.root.list_children:
            cur_subtree = Tree(leaf)
            cur_subtree.get_height()
            if cur_subtree.root.height > temp_height:
                temp_height = cur_subtree.root.height
        self.root._height += temp_height

        return self.root.height

    def from_list(self, lst: list) -> 'Tree':
        '''
        Builds a tree from a specific list:
        the values in the list point to the parent of the node in the tree
        indexes will be values of the tree
        >>>from_list([4, -1, 4, 1, 1])
                1
              3   4
                 0 2
        '''
        node_list = [Node(i) for i in range(len(lst))]

        for num, node in enumerate(node_list):
            if lst[num] == -1:
                self.root = node_list[num]
            else:
                node.set_parent(node_list[lst[num]])
        return Tree(self.root)


_ = sys.stdin.readline()
inp = [int(i) for i in sys.stdin.readline().split()]
mytree = Tree(None).from_list(inp)
print(mytree.get_height())
