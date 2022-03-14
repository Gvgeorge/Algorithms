from collections import deque
from typing import Callable
import sys


class Node:
    '''
    Represents a node of the AVL Tree.
    each node stores value, height sum of all values of nodes of its subtree
    '''
    def __init__(self, value: int, lc: 'Node' = None, rc: 'Node' = None):
        self._value = value
        self._parent = None
        self._lc = lc
        self._rc = rc
        self._height = 0
        self._summ = value
        if lc is not None:
            self._lc._parent = self
        if rc is not None:
            self._rc._parent = self
        if lc is not None and rc is not None:
            self._height = max(lc.height, rc.height) + 1
            self._summ += lc.summ + rc.summ
        elif lc is not None:
            self._height = lc.height + 1
            self._summ += lc.summ
        elif rc is not None:
            self._height = rc.height + 1
            self._summ += rc.summ

    def __eq__(self, other: 'Node') -> bool:
        if self is None and other is None:
            return True
        if self is None or other is None:
            return False
        return self.value == other.value

    def __gt__(self,  other: 'Node') -> bool:
        return self.value > other.value

    def __ge__(self,  other: 'Node') -> bool:
        return self.value >= other.value

    @property
    def height(self) -> int:
        '''Returns height of node's subtree'''
        return self._height

    @property
    def summ(self) -> int:
        '''Returns sum of node's subtree'''
        return self._summ

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

    def __str__(self):
        return f'Node of value {self.value}'

    def __repr__(self):
        return f'Node of value {self.value}'

    @value.setter
    def set_value(self, value: int) -> None:
        old_value = self.value
        self._value = value
        self.set_summ = self.summ - old_value + value

    @height.setter
    def set_height(self, height: int) -> None:
        self._height = height

    @summ.setter
    def set_summ(self, summ: int) -> None:
        self._summ = summ

    @left.setter
    def set_lc(self, other: 'Node') -> None:
        self._lc = other
        if other is not None:
            other.set_parent = self

    @right.setter
    def set_rc(self, other: 'Node') -> None:
        self._rc = other
        if other is not None:
            other.set_parent = self

    @parent.setter
    def set_parent(self, other: 'Node') -> None:
        if other is None:
            self._parent = other
            return
        self._parent = other
        if self.value < other.value:
            other._lc = self
        else:
            other._rc = self

    def update_height_single(self) -> None:
        '''Updates height of the current node only.'''
        if self.left and self.right:
            self.set_height = max(self.left.height, self.right.height) + 1
        elif self.right:
            self.set_height = self.right.height + 1
        elif self.left:
            self.set_height = self.left.height + 1
        else:  # case child was deleted
            self.set_height = 0

    def update_summ_single(self) -> None:
        '''Updates sum of the current node only.'''

        if self.left and self.right:
            self.set_summ = self.value \
                                   + self.left.summ \
                                   + self.right.summ
        elif self.right:
            self.set_summ = self.right.summ + self.value
        elif self.left:
            self.set_summ = self.left.summ + self.value
        else:
            self.set_summ = self.value

    def update_summ(self) -> None:
        '''updates bottom up log n'''
        while self:
            self.update_summ_single()
            self = self.parent

    def update_height(self) -> None:
        '''
        updates bottom up log n
        '''
        while self:
            self.update_height_single()
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


class AVLTree:
    '''
    Implementation of the AVL Tree
    '''
    def __init__(self, root: Node = None):
        self._root = root
        self.q = deque()

    @property
    def root(self) -> Node:
        '''Returns root'''
        return self._root

    @property
    def height(self) -> int:
        '''Returns height of the tree (height of the root node)'''
        if self.root is None:
            return 0
        return self.root._height

    @property
    def summ(self) -> int:
        '''Returns sum of the tree (sum of the root node)'''
        if self.root is None:
            return 0
        return self.root.summ

    def find(self, value: int) -> Node:
        '''
        Recursively searches for value from the root.
        Returns None if value is not in the tree.
        '''
        return self._find(self.root, value)

    def _find(self, root: Node, value: int) -> Node:
        '''
        Recursively searches for value from the node.
        Returns None if value is not in the tree.
        '''
        node = root
        while node is not None:
            if node.value == value:
                return node
            elif node.value < value:
                node = node.right
            else:
                node = node.left

    def _add(self, value: int) -> Node:
        '''
        Find the place to add the value into the tree
        and adds it without rebalancing the tree.
        Returns the newly created node with the input value
        '''
        new_node = Node(value)

        if self.root is None:
            self._root = new_node
            return new_node

        node = self.root

        while True:

            if value == node.value:
                # print('value already exists in the tree')
                return

            elif value < node.value:
                if node.left is None:
                    node.set_lc = new_node
                    break
                else:
                    node = node.left
            elif value > node.value:
                if node.right is None:
                    node.set_rc = new_node
                    break
                else:
                    node = node.right

        return new_node

    def balanced_add(self, value: int) -> Node:
        '''
        Adds with rebalance.
        Rebalances at the node the new value was inserted to.
        '''
        added = self._add(value)
        return self.rotate(added)

    def _remove(self, root: Node, value: int) -> Node:
        '''
        Finds the value in the tree and removes it without rebalance.
        Returns the parent of the removed node
        or None if value is not in the tree.
        '''
        target_node = self._find(root, value)
        if target_node is None:
            return None
        parent = target_node.parent
        # case leaf node
        if target_node.is_leaf():
            if target_node.is_root():
                self._root = None
                return self.root
            if parent.left is target_node:
                parent.set_lc = None
            elif parent.right is target_node:
                parent.set_rc = None
            target_node.set_parent = None

        # case single child
        # переподвешиваем вершину к свободному споту деда
        elif target_node.left is None:
            right = target_node.right
            right.set_parent = parent
            if parent is None:
                self._root = right
        elif target_node.right is None:
            left = target_node.left
            left.set_parent = parent
            if parent is None:
                self._root = left

        # case two children
        else:
            pred_node = AVLTree(target_node.right).get_min_node()
            self._swap(target_node, pred_node)
            return self._remove(pred_node, value)
        return parent

    def balanced_remove(self, value: int) -> Node:
        '''
        Removes the value from the tree and rebalances it
        bottom up starting at the parent of the value's node.
        '''
        node_to_balance = self._remove(self.root, value)
        self.rotate(node_to_balance)
        return node_to_balance

    def _swap(self, node_a: Node, node_b: Node) -> None:
        '''
        Swaps values of two nodes.
        '''
        node_a.set_value, node_b.set_value = node_b.value, node_a.value

    def get_min_node(self) -> Node:
        '''
        Returns the node with the minimum value of the tree
        '''
        root = self.root

        if root is None:
            return None

        while root.left is not None:
            root = root.left
        return root

    def get_max_node(self) -> Node:
        '''
        Returns the node with the maximum value of the tree
        '''
        root = self.root

        if root is None:
            return None

        while root.right is not None:
            root = root.right
        return root

    def get_next_node(self, value: int) -> Node:
        '''
        Finds the node with the given value, then finds
        the node next for it node.
        Returns None if either the value has not been found
        or there is no next node
        '''
        node = self.find(value)
        if not node:
            raise ValueError('value does not exist in a tree.')
        if node.right is not None:
            return AVLTree(node.right).get_min_node()
        else:
            old_node = node
            while node.parent:
                node = node.parent
                if node.value >= old_node.value:
                    return node
        if old_node.is_leaf() and node.is_root():
            return None

    def get_prev_node(self, value: int) -> Node:
        '''
        Finds the node with the given value, then finds
        the node before this node.
        Returns None if either the value has not been found
        or there is no previous node
        '''
        node = self.find(value)
        if not node:
            raise ValueError('value does not exist in a tree.')
        if node.left is not None:
            return AVLTree(node.left).get_max_node()
        else:
            old_node = node
            while node.parent:
                node = node.parent
                if node.value <= old_node.value:
                    return node
        if old_node.is_leaf() and node.is_root():
            return None

    def merge_with_root(self, other: 'AVLTree', root: Node) -> 'AVLTree':
        '''
        Merges two trees on with the root.
        All the values in the left tree (self) should be less than
        all the values in the right tree (other)
        Only returns a balanced AVL Tree if the difference between the
        heights of the trees is <= 1
        '''
        root_node = Node(root)
        root_node.set_lc = self.root
        root_node.set_rc = other.root
        root_node.update_height_single()
        root_node.update_summ_single()
        return AVLTree(root_node)

    def merge(self, other: 'AVLTree') -> 'AVLTree':
        '''
        Merges two AVL trees (T1 < T2)
        Only returns a balanced AVL Tree if the difference between the
        heights of the trees is <= 1
        '''
        if self.root is None:
            return other
        if other.root is None:
            return self
        if self.height >= other.height:
            max_val = self.get_max_node().value
            self.balanced_remove(max_val)
            merged = self.merge_with_root(other, max_val)
        else:
            min_val = other.get_min_node().value
            other.balanced_remove(min_val)
            merged = self.merge_with_root(other, min_val)
        return merged

    def AVLmerge(self, other) -> 'AVLTree':
        '''
        Merges two AVL Trees into one
        input trees can have any heights.
        '''
        if self.root is None:
            return other

        if other.root is None:
            return self

        if abs(self.height - other.height) <= 1:
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

            return self.AVLmerge(AVLTree(T)).AVLmerge(other)

        else:
            T = self.root
            while (T.height - other.height) > 1:
                T = T.right

            parent = T.parent
            if parent is not None:
                parent.set_rc = None
                T.set_parent = None
                self.rotate(parent)

            return self.AVLmerge(AVLTree(T).AVLmerge(other))

    def split(self, value: int) -> tuple['AVLTree', 'AVLTree']:
        '''
        Splits the current tree into two, left tree with values
        less than input value, right tree with values bigger or
        equal to input value
        '''
        avl_left = AVLTree()
        avl_right = AVLTree()
        cur_root = self.root
        while cur_root is not None:
            if value < cur_root.value:
                new_root = cur_root.left
                cur_root.set_lc = None
                if new_root is not None:
                    new_root.set_parent = None
                cur_tree = AVLTree(cur_root)
                cur_tree.rotate(cur_root)
                avl_right = cur_tree.AVLmerge(avl_right)

            else:
                new_root = cur_root.right
                cur_root.set_rc = None
                if new_root is not None:
                    new_root.set_parent = None
                cur_tree = AVLTree(cur_root)
                cur_tree.rotate(cur_root)
                avl_left = avl_left.AVLmerge(cur_tree)
            cur_root = new_root
        return avl_left, avl_right

    def rotate_right(self, node: Node) -> Node:
        '''
        Performs right rotation for the subtree at a given node.
        '''
        new_root = node.left
        if node.is_root():
            self._root = new_root
        right_child = new_root.right
        node.set_lc = None
        new_root.set_parent = node.parent
        new_root.set_rc = None
        if right_child:
            right_child.set_parent = None
        node.set_lc = right_child
        new_root.set_rc = node
        node.update_height_single()
        node.update_summ_single()
        return new_root

    def rotate_left(self, node: Node) -> Node:
        '''
        Performs left rotation for the subtree at a given node.
        '''
        new_root = node.right
        if node.is_root():
            self._root = new_root
        left_child = new_root.left
        node.set_rc = None
        new_root.set_parent = node.parent
        new_root.set_lc = None
        if left_child:
            left_child.set_parent = None
        node.set_rc = left_child
        new_root.set_lc = node
        node.update_height_single()
        node.update_summ_single()
        return new_root

    def rotate_left_right(self, node: Node) -> Node:
        '''
        Performs left right rotation for the subtree at a given node.
        '''
        left = node.left
        node.set_lc = self.rotate_left(left)
        node.update_height_single()
        node.update_summ_single()
        return self.rotate_right(node)

    def rotate_right_left(self, node: Node) -> Node:
        '''
        Performs right left rotation for the subtree at a given node.
        '''
        right = node.right
        node.set_rc = self.rotate_right(right)
        node.update_height_single()
        node.update_summ_single()
        return self.rotate_left(node)

    def choose_rotation(self, node: Node) -> Callable:
        '''
        Returns the correct function to rotate the subtree
        with root at a given node.
        Returns None if this subtree is balanced
        '''
        if not node.right:
            rh = 0
        else:
            rh = node.right.height + 1
        if not node.left:
            lh = 0
        else:
            lh = node.left.height + 1

        if rh - lh >= 2:
            rc = node.right
            if not rc.left:
                rclh = 0
            else:
                rclh = rc.left.height + 1
            if not rc.right or rclh > rc.right.height + 1:
                return self.rotate_right_left
            else:
                return self.rotate_left
        elif lh - rh >= 2:
            lc = node.left
            if not lc.right:
                lcrh = 0
            else:
                lcrh = lc.right.height + 1
            if not lc.left or lcrh > lc.left.height + 1:
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
            node.update_summ_single()
            node = node.parent

    def find_lower_bound(self, value: int) -> Node:
        '''
        Returns node with the lowest value that is
        higher or equal to input value
        '''

        node = self.root
        candidate = None
        while node is not None:
            if node.is_leaf() or node.value == value:
                break

            if node.value > value:
                candidate = node
                if node.left is not None:
                    node = node.left
                else:
                    node = node.right
            else:
                if node.right is not None:
                    node = node.right
                else:
                    break
        if candidate is None or candidate.value < value:
            if node.value >= value:
                return node
            return None
        if node is None or node.value < value:
            return candidate

        if candidate.value >= value and node.value >= value:
            return candidate if candidate < node else node

    def find_higher_bound(self, value: int) -> Node:
        '''
        Returns node with the highest value that is
        lower or equal to input value
        '''

        node = self.root
        candidate = None
        while node is not None:
            if node.is_leaf() or node.value == value:
                break

            if node.value < value:
                candidate = node
                if node.right is not None:
                    node = node.right
                else:
                    node = node.left
            else:
                if node.left is not None:
                    node = node.left
                else:
                    break
        if candidate is None or candidate.value > value:
            if node.value <= value:
                return node
            return None
        if node is None or node.value > value:
            return candidate

        if candidate.value <= value and node.value <= value:
            return candidate if candidate > node else node

    def find_closest_common_ancestor(self, node_a: Node, node_b: Node) -> Node:
        '''
        returns a closest ancestor of node a and node b
        if no such ancestor exists returns None
        '''
        ancestors = set()
        while node_b is not None:
            ancestors.add(node_b.value)
            node_b = node_b.parent
        while node_a is not None:
            if node_a.value in ancestors:
                return node_a
            node_a = node_a.parent

    def find_summ(self, a: int, b: int) -> int:
        '''
        Calculates the sum of the values in the tree
        between numbers a and b.
        '''
        if self.root is None:
            return 0

        if a > b:
            a, b = b, a
        left_bound = self.find_lower_bound(a)
        right_bound = self.find_higher_bound(b)
        if left_bound is None or right_bound is None:
            return 0
        if left_bound == right_bound:
            return left_bound.value
        if right_bound < left_bound:
            return 0

        local_root = self.find_closest_common_ancestor(left_bound, right_bound)

        if left_bound.left is None:
            left_sub = 0
        else:
            left_sub = left_bound.left.summ

        if right_bound.right is None:
            right_sub = 0
        else:
            right_sub = right_bound.right.summ

        summ = local_root.summ - left_sub - right_sub

        if left_bound != local_root:
            while left_bound.parent < local_root:
                if left_bound.parent.value < a:
                    summ -= left_bound.parent.summ
                    summ += left_bound.summ
                left_bound = left_bound.parent

        if right_bound != local_root:

            while right_bound.parent > local_root:

                if right_bound.parent.value > b:
                    summ -= right_bound.parent.summ
                    summ += right_bound.summ
                right_bound = right_bound.parent

        return summ

    def pre_order(self) -> list:
        '''
        Recursively pushes values from the tree to list
        pre order
        '''
        lst = []

        def _pre_order(node):
            if node is None:
                return
            lst.append(node.value)
            _pre_order(node.left)
            _pre_order(node.right)
            return lst

        return _pre_order(self.root)

    def in_order(self) -> list:
        '''
        Recursively pushes values from the tree to list
        in order
        '''

        lst = []

        def _in_order(node):
            if node is None:
                return
            _in_order(node.left)
            lst.append(node.value)
            _in_order(node.right)
            return lst
        return _in_order(self.root)

    def post_order(self) -> list:
        '''
        Recursively pushes values from the tree to list
        post order
        '''

        lst = []

        def _post_order(node):
            if node is None:
                return
            _post_order(node.left)
            _post_order(node.right)
            lst.append(node.value)
            return lst

        return _post_order(self.root)

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


def parse_sums(string: str):
    res = string.strip().split('\n')[1:]
    bst = AVLTree()
    summ = 0
    for inp in res:
        if inp.startswith('?'):
            found = bst.find(get_mod_of_sum(int(inp.split()[1]), summ))
            if found is None:
                print('Not found')
            else:
                print('Found')
        elif inp.startswith('+'):
            val = get_mod_of_sum(int(inp.split()[1]), summ)
            bst.balanced_add(val)
        elif inp.startswith('-') or inp.startswith('-'):
            val = get_mod_of_sum(int(inp.split()[1]), summ)
            bst.balanced_remove(val)
        else:
            bounds = inp.split()
            lower_bound = get_mod_of_sum(int(bounds[1]), summ)
            upper_bound = get_mod_of_sum(int(bounds[2]), summ)
            summ = bst.find_summ(lower_bound, upper_bound)
            print(summ)


def get_mod_of_sum(x: int, summ: int) -> int:
    return (x + summ) % 1000000001


if __name__ == '__main__':
    inp = sys.stdin.read()
    parse_sums(inp)
