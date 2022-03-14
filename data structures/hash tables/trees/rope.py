from collections import deque
from typing import Callable
import sys


class Node:
    '''
    Represents a node of the Rope.
    each node stores value, height of its subtree and
    size - sum of all values of nodes of its subtree
    '''
    def __init__(self, value: str, lc: 'Node' = None, rc: 'Node' = None):
        '''
        height represents the height of the nodes subtree
        size - the number of nodes in the subtree
        '''
        self._value = value
        self._parent = None
        self._lc = lc
        self._rc = rc
        self._height = 0
        if self.value is not None:
            self._size = len(self.value)
        else:
            self._size = 0
        if lc is not None:
            self._lc._parent = self
        if rc is not None:
            self._rc._parent = self
        if lc is not None and rc is not None:
            self._height = max(lc.height, rc.height) + 1
            self._size = lc.size + rc.size
        elif lc is not None:
            self._height = lc.height + 1
            self._size = lc.size
        elif rc is not None:
            self._height = rc.height + 1
            self._size = rc.size

    def __eq__(self, other):
        if self is None and other is None:
            return True
        if self is None or other is None:
            return False
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    @property
    def height(self) -> int:
        '''Returns height of node's subtree'''
        return self._height

    @property
    def size(self) -> int:
        '''returns the number of nodes in nodes's subtree'''
        return self._size

    @property
    def value(self) -> int:
        '''Returns node's value'''
        return self._value

    @property
    def left(self) -> 'Node':
        '''Returns node's left child'''
        return self._lc

    @property
    def right(self) -> 'Node':
        '''Returns node's right child'''
        return self._rc

    @property
    def parent(self) -> 'Node':
        '''Returns node's parent'''
        return self._parent

    @value.setter
    def set_value(self, value: str):
        self._value = value

    @height.setter
    def set_height(self, height: int):
        self._height = height

    @size.setter
    def set_size(self, size: int):
        self._size = size

    @left.setter
    def set_lc(self, other):
        self._lc = other
        if other is not None:
            other.set_parent = self

    @right.setter
    def set_rc(self, other):
        self._rc = other
        if other is not None:
            other.set_parent = self

    @parent.setter
    def set_parent(self, other):
        if other is None:
            self._parent = other
            return
        self._parent = other

    def update_height_single(self) -> None:
        if self.left is not None and self.right is not None:
            self.set_height = max(self.left.height, self.right.height) + 1
        elif self.right is not None:
            self.set_height = self.right.height + 1
        elif self.left is not None:
            self.set_height = self.left.height + 1
        else:  # case child was deleted
            self.set_height = 0

    def update_height(self) -> None:
        '''
        Updates height of a node and all its parents bottom up
        '''
        while self:
            self.update_height_single()
            self = self.parent

    def update_size_single(self) -> None:
        '''
        Updates size of a single node
        '''
        if self.is_leaf():
            self.set_size = len(self.value)
        if self.right is not None and self.left is not None:
            self.set_size = self.left.size + self.right.size
        elif self.left is not None:
            self.set_size = self.left.size
        elif self.right is not None:
            self.set_size = self.right.size

    def update_size(self) -> None:
        '''
        Updates size of a node and all its parents bottom up
        '''
        while self:
            self.update_size_single()
            self = self.parent

    def is_leaf(self) -> bool:
        '''Checks if node has children'''
        if self.left is None and self.right is None:
            return True
        return False

    def is_root(self) -> bool:
        '''Checks if node is root'''
        if self.parent is None:
            return True
        return False

    def __str__(self):
        return f'Node of value {self.value}'

    def __repr__(self):
        return f'Node of value {self.value}'


class Rope:
    '''
    Rope data structure based on AVL tree
    '''
    def __init__(self, root=None):
        self._root = root

    def __eq__(self, other):
        if self.root != other.root:
            return False
        if not self.root and not other.root:
            return True
        compare_left = Rope(self.root.left) == Rope(other.root.left)
        compare_right = Rope(self.root.right) == Rope(other.root.right)

        return compare_left and compare_right

    def __getitem__(self, idx: int) -> str:
        if idx > self.root.size:
            raise IndexError

        node = self.root
        while True:
            if node.is_leaf():
                return node.value[idx]
            if node.left.size >= idx:
                node = node.left
            else:
                idx = idx - node.left.size
                node = node.right

    @property
    def root(self) -> Node:
        return self._root

    @property
    def size(self) -> int:
        if self.root is None:
            return 0
        return self.root._size

    @property
    def height(self) -> int:
        if self.root is None:
            return 0
        return self.root._height

    def _remove_node(self, root: Node, node: Node) -> Node:
        '''
        Finds the value in the tree and removes it without rebalance.
        Returns the parent of the removed node
        or None if value is not in the tree.
        '''

        if node is None:
            return None
        parent = node.parent
        # case leaf node
        if node.is_leaf():
            if node.is_root():
                self._root = None
                return self.root
            if parent.left is node:
                parent.set_lc = None
            elif parent.right is node:
                parent.set_rc = None
            node.set_parent = None

        # case single child
        # переподвешиваем вершину к свободному споту деда
        elif node.left is None:
            right = node.right
            right.set_parent = parent
            if parent is None:
                self._root = right
            elif node.parent.left is node:
                parent.set_lc = right
            elif node.parent.right is node:
                parent.set_rc = right
            node.set_parent = None

        elif node.right is None:
            left = node.left
            left.set_parent = parent
            if parent is None:
                self._root = left
            elif node.parent.left is node:
                parent.set_lc = left
            elif node.parent.right is node:
                parent.set_rc = left
            node.set_parent = None

        # case two children
        else:
            pred_node = Rope(node.right).get_min_node()
            self._swap(node, pred_node)
            return self._remove_node(node, pred_node)
        return parent

    def balanced_remove_node(self, node: Node) -> Node:
        '''
        Removes the value from the tree and rebalances it
        bottom up starting at the parent of the value's node.
        '''
        node_to_balance = self._remove_node(self.root, node)
        self.rotate(node_to_balance)
        return node_to_balance

    def _swap(self, node_a, node_b):
        '''
        Swaps values of two nodes.
        '''
        node_a.set_value, node_b.set_value = node_b.value, node_a.value

    def get_min_node(self) -> Node:
        '''
        Returns the leftmost node of the rope
        '''
        root = self.root

        if root is None:
            return None

        while root.left is not None:
            root = root.left
        return root

    def get_max_node(self) -> Node:
        '''
        Returns the rightmost node of the rope
        '''
        root = self.root

        if root is None:
            return None

        while root.right is not None:
            root = root.right
        return root

    def _split_node_by_idx(self, node: Node, idx: int) -> 'Rope':
        '''
        Splits the string within a node into two substrings
        each in a separate node by idx.
        >>>rope = Rope().convert_from_string(abcdefghijk)
        >>rope.print_tree()
        ['abcdefghijk']
        ['$', '$']
        >>rope = rope._split_node_by_idx(rope.root, 4)
        >>rope.print_tree()
        [11]
        ['abcd', 'efghijk']
        ['$', '$', '$', '$']
        '''
        if idx == len(node.value):
            right = Rope()
        else:
            right = Rope(Node(node.value[idx:]))

        if idx == 0:
            left = Rope()
        else:
            left = Rope(Node(node.value[:idx]))
        return left.merge(right)

    def split_by_idx(self, idx: int) -> tuple['Rope', 'Rope']:
        '''
        Splits rope by idx into two ropes
        >>>rope = Rope().convert_from_string(abcdefghijk)
        >>rope.print_tree()
        ['abcdefghijk']
        ['$', '$']
        >>left, right = rope.split_by_idx(4)
        >>left.print_tree()
        ['abcd']
        ['$', '$']
        >>right.print_tree()
        ['efghijk']
        ['$', '$']
        '''
        if idx == 0:
            return (Rope(), self)
        if idx == self.root.size:
            return (self, Rope())

        avl_left = Rope()
        avl_right = Rope()

        cur_root = self.root
        while cur_root is not None:
            if cur_root.left is None:
                left_size = 0
            else:
                left_size = cur_root.left.size

            if cur_root.is_leaf():
                cur_root_val = cur_root.value
                if idx == 0:
                    right_substring_rope = Rope().convert_from_string(
                        cur_root_val)
                    avl_right = right_substring_rope.AVLmerge(avl_right)
                elif idx == len(cur_root_val):
                    cur_tree = Rope(cur_root)
                    cur_tree.rotate(cur_root)
                    avl_left = avl_left.AVLmerge(cur_tree)
                else:
                    split_rope = self._split_node_by_idx(cur_root, idx)
                    split_leaf = split_rope.root
                    parent = cur_root.parent
                    if parent is None:
                        cur_root = split_leaf
                        continue
                    if cur_root is parent.left:
                        parent.set_lc = split_leaf
                        split_leaf.set_parent = parent
                    elif cur_root is parent.right:
                        parent.set_rc = split_leaf
                        split_leaf.set_parent = parent
                    else:
                        raise AttributeError

                    cur_root = split_leaf
                    continue
                break

            if idx <= left_size:
                new_root = cur_root.left
                cur_root.set_lc = None
                if new_root is not None:
                    new_root.set_parent = None
                cur_tree = Rope(cur_root)
                cur_tree.rotate(cur_root)
                avl_right = cur_tree.AVLmerge(avl_right)
            else:
                idx -= left_size
                new_root = cur_root.right
                cur_root.set_rc = None
                if new_root is not None:
                    new_root.set_parent = None
                cur_tree = Rope(cur_root)
                cur_tree.rotate(cur_root)

                avl_left = avl_left.AVLmerge(cur_tree)
            cur_root = new_root
        return avl_left, avl_right

    def _flatten(self, node: Node) -> Node:
        '''
        Removes unnecessary nodes in the middle of tree
        >>rope.print_tree()
        [11]
        ['abcd', 7]
        ['$', '$', '$', 'efghijk']
        By calling _flatten on node with value 7 we remove it from the
        tree without damaging the tree
        >>rope._flatten(rope.root.right)
        [11]
        ['abcd', 'efghijk']
        '''
        if node.value == '':
            if (node.left is None) != (node.right is None):
                self.balanced_remove_node(node)

    def merge(self, other) -> 'Rope':
        '''
        Merges two ropes together. Doesn't balance them.
        Only returns a balanced Rope if the difference between the
        heights of the trees is <= 1
        '''
        if self.root is None:
            return other
        if other.root is None:
            return self

        root = Node('')
        root.set_lc = self.root
        root.set_rc = other.root
        root.update_height_single()
        root.update_size_single()
        return Rope(root)

    def AVLmerge(self, other) -> 'Rope':
        '''
        Merges two Ropes into one, balances them
        input trees can have any heights.
        '''
        if self.root is None:
            return other

        if other.root is None:
            return self

        if abs(self.height - other.height) <= 2:
            return self.merge(other)

        if other.height > self.height:
            T = other.root
            while (T.height - self.height) > 1:
                T = T.left

            parent = T.parent

            if parent is not None:

                parent.set_lc = None
                T.set_parent = None
                other.rotate(parent)

            return self.AVLmerge(Rope(T)).AVLmerge(other)

        else:
            T = self.root
            while (T.height - other.height) > 1:
                T = T.right

            parent = T.parent

            if parent is not None:
                parent.set_rc = None
                T.set_parent = None
                self.rotate(parent)

            return self.AVLmerge(Rope(T).AVLmerge(other))

    def rotate_right(self, node: Node) -> Node:
        '''
        Performs right rotation for the subtree at a given node.
        '''
        new_root = node.left
        right_child = new_root.right
        node.set_lc = None
        if node.is_root():
            self._root = new_root
            new_root.set_parent = None
        else:
            if node.parent.left is node:
                node.parent.set_lc = new_root
            else:
                node.parent.set_rc = new_root

            new_root.set_parent = node.parent

        new_root.set_rc = None

        if right_child is not None:
            right_child.set_parent = None
        node.set_lc = right_child
        new_root.set_rc = node
        node.update_height_single()
        node.update_size_single()
        return new_root

    def rotate_left(self, node: Node) -> Node:
        '''
        Performs left rotation for the subtree at a given node.
        '''
        new_root = node.right
        left_child = new_root.left
        node.set_rc = None

        if node.is_root():
            self._root = new_root
            new_root.set_parent = None
        else:
            if node.parent.left is node:
                node.parent.set_lc = new_root
            else:
                node.parent.set_rc = new_root

            new_root.set_parent = node.parent

        new_root.set_lc = None
        if left_child is not None:
            left_child.set_parent = None
        node.set_rc = left_child
        new_root.set_lc = node
        node.update_height_single()
        node.update_size_single()

        return new_root

    def rotate_left_right(self, node: Node) -> Node:
        '''
        Performs left right rotation for the subtree at a given node.
        '''
        left = node.left
        node.set_lc = self.rotate_left(left)
        node.update_height_single()
        node.update_size_single()

        return self.rotate_right(node)

    def rotate_right_left(self, node: Node) -> Node:
        '''
        Performs right left rotation for the subtree at a given node.
        '''
        right = node.right
        node.set_rc = self.rotate_right(right)
        node.update_height_single()
        node.update_size_single()
        return self.rotate_left(node)

    def choose_rotation(self, node: Node) -> Callable:
        '''
        Returns the correct function to rotate the subtree
        with root at a given node.
        Returns None if this subtree is balanced
        '''
        if node.right is None:
            rh = 0
        else:
            rh = node.right.height + 1
        if node.left is None:
            lh = 0
        else:
            lh = node.left.height + 1

        if rh - lh >= 2:
            rc = node.right
            if rc.left is None:
                rclh = 0
            else:
                rclh = rc.left.height + 1
            if rc.right is None or rclh > rc.right.height + 1:
                return self.rotate_right_left
            else:
                return self.rotate_left
        elif lh - rh >= 2:
            lc = node.left
            if lc.right is None:
                lcrh = 0
            else:
                lcrh = lc.right.height + 1
            if lc.left is None or lcrh > lc.left.height + 1:
                return self.rotate_left_right
            else:
                return self.rotate_right

    def rotate(self, node: Node) -> None:
        '''
        Rotates the subtree with root at a given node
        '''
        while node is not None:
            rotation = self.choose_rotation(node)
            while rotation is not None:
                rotation(node)
                rotation = self.choose_rotation(node)
            node.update_height_single()
            node.update_size_single()

            prev_node = node
            self._flatten(prev_node)
            node = node.parent

    def print_tree(self) -> None:
        '''Prints the tree'''
        root = self.root
        buf = deque()
        output = []
        if not root:
            print('$')
        else:
            buf.append(root)
            count, nextCount = 1, 0
            while count:
                node = buf.popleft()
                if node:
                    if node.value == '':
                        output.append(node.size)
                    else:
                        output.append(node.value)
                    count -= 1
                    for n in (node.left, node.right):
                        if n:
                            buf.append(n)
                            nextCount += 1
                        else:
                            buf.append(None)
                else:
                    output.append('$')
                if not count:
                    print(output)
                    output = []
                    count, nextCount = nextCount, 0
            # print the remaining all empty leaf node part
            output.extend(['$']*len(buf))
            print(output)

    def convert_from_string(self, string: str) -> 'Rope':
        '''Converts a string into a rope'''
        self._root = Node(string)
        return self

    def convert_to_list(self) -> list:
        '''Converts a rope into list'''
        lst = []

        def _convert_to_list(node: Node) -> list:
            if node is None:
                return
            _convert_to_list(node.left)
            if node.value:
                lst.append(node.value)
            _convert_to_list(node.right)
            return lst
        return _convert_to_list(self.root)


def parse(input_string):
    input_list = input_string.strip().split('\n')
    string = input_list[0]
    rope = Rope().convert_from_string(string)
    actions = input_list[2:]
    for action in actions:

        left_bound, right_bound, insert_idx = [int(i) for i in action.split()]
        right_bound -= left_bound - 1
        left, right = rope.split_by_idx(left_bound)
        mid, right = right.split_by_idx(right_bound)
        rope = left.AVLmerge(right)
        left, right = rope.split_by_idx(insert_idx)
        rope = left.AVLmerge(mid).AVLmerge(right)
    print(''.join(rope.convert_to_list()))


if __name__ == '__main__':
    parse(sys.stdin.read())
