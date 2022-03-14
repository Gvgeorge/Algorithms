from AVLTree import Node, AVLTree as BaseAVLTree
import AVLTestsData as td
from collections import deque
from copy import deepcopy
import bisect
import random
import unittest


class AVLTree(BaseAVLTree):
    def __eq__(self, other):
        if self.root != other.root:
            return False
        if not self.root and not other.root:
            return True
        compare_left = AVLTree(self.root.left) == AVLTree(other.root.left)
        compare_right = AVLTree(self.root.right) == AVLTree(other.root.right)
        return compare_left and compare_right

    def add(self, value: int) -> int:
        '''Adds a value into the tree without rebalance'''
        added = self._add(value)
        if added:
            added.update_height()
            added.update_summ()
        return added

    def remove(self,  value: int) -> int:
        '''Removes a value into the tree without rebalance'''
        node_to_balance = self._remove(self.root, value)
        if node_to_balance is not None:
            node_to_balance.update_height()
            node_to_balance.update_summ()
        return node_to_balance

    def is_correct(self) -> bool:
        '''
        Checks whether the tree is correct (no repeats)
        '''
        in_order = self.in_order()
        if self.root is None:
            return True
        return all([in_order[i] < in_order[i+1]
                    for i in range(len(in_order)-1)])

    def is_correct_wrepeats(self) -> bool:
        '''
        Checks whether the tree is correct (with repeats)
        '''
        return self._is_correct_wrepeats(self.root)

    def _is_correct_wrepeats(self, root):

        if root.left:
            self.q.appendleft(root.left)
            max_left = AVLTree(root.left).get_max_node()
            if root <= max_left:
                return False

        if root.right:
            self.q.appendleft(root.right)
            min_right = AVLTree(root.right).get_min_node()
            if root > min_right:
                return False
        while self.q:
            return self._is_correct_wrepeats(self.q.pop())

        return True

    def is_balanced(self):
        '''Checks whether the tree is balanced'''
        if self.root is None:
            return True
        return self._is_balanced(self.root)

    def _is_balanced(self, node):
        if not node.left and not node.right:
            return True
        if not node.left:
            left_height = 0
        else:
            left_height = node.left.height + 1
        if not node.right:
            right_height = 0
        else:
            right_height = node.right.height + 1

        if abs(left_height - right_height) > 1:
            return False
        else:
            if not node.right:
                return self._is_balanced(node.left)
            elif not node.left:
                return self._is_balanced(node.right)
            left_is_balanced = self._is_balanced(node.left)
            right_is_balanced = self._is_balanced(node.right)
            return left_is_balanced and right_is_balanced

    def calculate_height(self) -> int:
        '''
        Calculates the height of the tree starting from the root.
        ineffective but useful
        '''
        root = self.root
        if root.is_leaf():
            root.set_height = 0
            return root.height
        if root.left and root.right:
            AVLTree(root.right).calculate_height()
            AVLTree(root.left).calculate_height()
            root.set_height = max(root.right.height, root.left.height) + 1
        elif root.left:
            AVLTree(root.left).calculate_height()
            root.set_height = root.left.height + 1
        elif root.right:
            AVLTree(root.right).calculate_height()
            root.set_height = root.right.height + 1
        return root.height

    def from_list(self, lst: list) -> 'AVLTree':
        for item in lst:
            self.balanced_add(item)
        return self

    def print_tree(self) -> None:
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


def bisect_sum(lst, a, b):
    '''
    returns a  sum of items in a lst from a to b
    '''
    if a > b:
        a, b = b, a
    lst = sorted(lst)
    a = bisect.bisect_left(lst, a)
    b = bisect.bisect_right(lst, b)
    return sum(lst[a:b])


def parse(string: str) -> tuple[int, Node]:
    '''
    Function for parsing strings from AVLTestsData module
    '''
    string = string.strip().split('\n')
    num_nodes, nodes = string[0], string[1:]
    nodes = [node.split() for node in nodes]
    nodes = [list(map(int, node)) for node in nodes]
    nodes = [list(map(lambda x: None if x == -1 else x, node))
             for node in nodes]

    def list_to_node(node):
        if node[1] is None and node[2] is None:
            return Node(node[0])
        elif node[1] is None:
            return Node(node[0], None, list_to_node(nodes[node[2]]))
        elif node[2] is None:
            return Node(node[0], list_to_node(nodes[node[1]]), None)
        return Node(node[0], list_to_node(nodes[node[1]]),
                    list_to_node(nodes[node[2]]))

    if not nodes:
        return 0, None
    root = list_to_node(nodes[0])
    return num_nodes, root


class TestNode(unittest.TestCase):
    def setUp(self):
        self.anode = Node(3, Node(2), Node(4))

    def test_get_lc(self):
        self.assertEqual(self.anode.left, Node(2))

    def test_get_rc(self):
        self.assertEqual(self.anode.right, Node(4))

    def test_get_value(self):
        self.assertEqual(self.anode.value, 3)

    def test_get_parent(self):
        self.assertEqual(self.anode.left.parent, self.anode)

    def test_get_sum(self):
        self.assertEqual(self.anode.summ, 9)

    def test_get_height(self):
        self.assertEqual(Node(2).height, 0)
        self.assertEqual(self.anode.height, 1)

    def test_set_value(self):
        self.anode.set_value = 10
        self.assertEqual(self.anode.value, 10)

    def test_set_lc(self):
        self.anode.set_lc = Node(5)
        self.assertEqual(self.anode.left, Node(5))
        self.anode.left.set_lc = Node(-1)
        self.assertEqual(self.anode.left.left, Node(-1))

    def test_set_rc(self):
        self.anode.set_rc = Node(0)
        self.assertEqual(self.anode.left, Node(0))
        self.anode.right.set_lc = Node(4)
        self.assertEqual(self.anode.right.left, Node(4))

    def test_set_parent(self):
        self.anode.set_parent = Node(3.5)
        self.assertEqual(self.anode.parent, Node(3.5))
        self.assertEqual(self.anode.parent.left, self.anode)
        self.assertEqual(self.anode.parent.right, None)

    def test_set_height(self):
        self.anode.set_height = 10
        self.assertEqual(self.anode.height, 10)
        self.anode.update_height()
        self.anode.set_rc = Node(20)
        self.assertEqual(self.anode.height, 1)
        self.anode.right.set_rc = Node(30)
        self.anode.right.update_height()
        self.assertEqual(self.anode.height, 2)
        node = Node(10, Node(5, Node(4), Node(7)),
                    Node(20, Node(15), Node(25)))
        self.assertEqual(node.height, 2)
        left = Node(-1, Node(-2, Node(-3)))
        self.assertEqual(left.height, 2)
        node.left.left.set_lc = left
        node.left.left.left.update_height()
        self.assertEqual(node.height, 5)

    def test_set_summ(self):
        node = Node(2, Node(1), Node(3))
        self.assertEqual(node.summ, 6)
        node.set_rc = None
        node.update_summ()
        node.update_height()
        self.assertEqual(node.summ, 3)

        node = Node(10, Node(5, Node(4), Node(7)),
                    Node(20, Node(15), Node(25)))
        self.assertEqual(node.summ, 86)
        left = Node(-1, Node(-2, Node(-3)))
        self.assertEqual(left.summ, -6)
        node.left.left.set_lc = left
        node.left.left.left.update_height()
        node.left.left.left.update_summ()
        self.assertEqual(node.summ, 80)

    def test_comparisons(self):
        self.assertEqual(None, None)
        self.assertNotEqual(Node(3), None)
        self.assertNotEqual(None, Node(3))
        self.assertEqual(Node(3), Node(3))
        self.assertGreater(Node(4), Node(3))
        self.assertGreaterEqual(Node(4), Node(3))
        self.assertLessEqual(Node(1), Node(1))
        self.assertNotEqual(None, Node(None))
        self.assertTrue(Node(-1))
        self.assertTrue(Node(0))


class TestAVLTree(unittest.TestCase):
    def setUp(self):
        node = Node(10)
        self.bst = AVLTree(node)
        self.bst.add(20)
        self.bst.add(30)
        self.bst.add(5)
        self.bst.add(7)

    def test_eq(self):
        bst = AVLTree(Node(1))
        bstx = AVLTree(Node(1))
        self.assertEqual(bst, bstx)
        bst = AVLTree(Node(1, Node(0), Node(2)))
        self.assertNotEqual(bst, bstx)
        bstx = AVLTree(Node(1, Node(0), Node(2)))
        self.assertEqual(bst, bstx)
        bstx = AVLTree(Node(1, Node(0, Node(-1)), Node(2)))
        self.assertNotEqual(bst, bstx)

    def test_add(self):
        self.assertEqual(self.bst.root.right.value, 20)
        self.assertEqual(self.bst.root.right.right, Node(30))
        self.assertEqual(self.bst.root.left, Node(5))
        self.assertEqual(self.bst.root.left.right.value, 7)
        self.bst.add(6)
        self.assertEqual(self.bst.root.left.right.left.value, 6)
        node_40 = Node(40)
        self.assertEqual(self.bst.add(40), node_40)
        bst = AVLTree()
        bst.add(6)
        self.assertEqual(bst.root, Node(6))

    def test_find(self):
        self.assertEqual(self.bst.find(10), self.bst.root)
        self.assertEqual(AVLTree().find('x'), None)
        res = self.bst.find(7)
        self.assertEqual(res, Node(7))

    def test_min(self):
        self.assertEqual(self.bst.get_min_node(), Node(5))
        bst = AVLTree(Node(3, Node(3), None))
        self.assertEqual(bst.get_min_node(), Node(3))

    def test_max(self):
        self.assertEqual(self.bst.get_max_node(), Node(30))
        bst = AVLTree(Node(3, Node(3), None))
        self.assertEqual(bst.get_max_node(), Node(3))

    def test_remove(self):
        self.bst.remove(30)
        self.assertEqual(self.bst.root.right.right, None)
        self.bst.add(30)
        self.bst.remove(5)
        self.assertEqual(self.bst.root.left.left, None)
        self.bst.add(6)
        self.bst.add(8)
        self.bst.remove(7)
        self.assertEqual(self.bst.root.left.right, None)
        self.assertEqual(self.bst.root.left.value, 8)
        self.bst.remove(10)
        self.assertEqual(self.bst.root.value, 20)
        self.assertEqual(self.bst.remove(6), Node(8))
        bst = AVLTree(None)
        bst.add(0)
        bst.remove(0)
        self.assertEqual(bst, AVLTree(None))
        bst.add(0)
        bst.add(1)
        bst.remove(0)
        self.assertEqual(bst, AVLTree(Node(1)))

    def test_swap(self):
        node_10 = self.bst.find(10)
        node_5 = self.bst.find(5)
        self.bst._swap(node_10, node_5)
        self.assertEqual(node_10.value, 5)
        self.assertEqual(node_5.value, 10)

    def test_next(self):
        bst = AVLTree(Node(20, Node(10, Node(5, Node(4, Node(3.5)),
                      Node(7)), Node(15, Node(12), Node(17))),
                      Node(30, Node(25, Node(24), Node(27)),
                           Node(35, Node(32), Node(40)))))

        self.assertEqual(bst.get_next_node(10).value, 12)
        self.assertEqual(bst.get_next_node(15).value, 17)
        self.assertEqual(bst.get_next_node(3.5).value, 4)
        self.assertEqual(bst.get_next_node(40), None)
        self.assertEqual(bst.get_next_node(27).value, 30)
        self.assertEqual(bst.get_next_node(20).value, 24)

        self.assertEqual(bst.get_next_node(30).value, 32)
        bst.balanced_remove(32)
        self.assertEqual(bst.get_next_node(30).value, 35)
        self.assertRaises(ValueError, bst.get_next_node, 90)

    def test_prev(self):
        bst = AVLTree(Node(20, Node(10, Node(5, Node(4, Node(3.5)), Node(7)),
                      Node(15, Node(12), Node(17))),
                           Node(30, Node(25, Node(24), Node(27)),
                                Node(35, Node(32), Node(40)))))

        self.assertEqual(bst.get_prev_node(12).value, 10)
        self.assertEqual(bst.get_prev_node(17).value, 15)
        self.assertEqual(bst.get_prev_node(4).value, 3.5)
        self.assertEqual(bst.get_prev_node(3.5), None)
        self.assertEqual(bst.get_prev_node(30).value, 27)
        self.assertEqual(bst.get_prev_node(24).value, 20)
        self.assertRaises(ValueError, bst.get_prev_node, 90)

    def test_is_correct(self):
        bst = AVLTree(parse(td.str_3)[1])
        self.assertTrue(bst.is_correct())
        bst = AVLTree(parse(td.str_4)[1])
        self.assertFalse(bst.is_correct())
        bst = AVLTree(parse(td.str_5)[1])
        self.assertTrue(bst.is_correct())
        bst = AVLTree(parse(td.str_6)[1])
        self.assertTrue(bst.is_correct())
        bst = AVLTree(parse(td.str_7)[1])
        self.assertFalse(bst.is_correct())
        self.assertTrue(AVLTree(parse('0')[1]).is_correct)

    def test_is_correct_wrepeats(self):
        bst = AVLTree(parse(td.str_3)[1])
        self.assertTrue(bst.is_correct_wrepeats())
        bst = AVLTree(parse(td.str_4)[1])
        self.assertFalse(bst.is_correct_wrepeats())
        bst = AVLTree(parse(td.str_8)[1])
        self.assertTrue(bst.is_correct_wrepeats())
        bst = AVLTree(parse(td.str_9)[1])
        self.assertFalse(bst.is_correct_wrepeats())
        bst = AVLTree(parse(td.str_10)[1])
        self.assertTrue(bst.is_correct_wrepeats())
        bst = AVLTree(parse(td.str_5)[1])
        self.assertTrue(bst.is_correct_wrepeats())
        bst = AVLTree(parse(td.str_5)[1])
        self.assertTrue(bst.is_correct_wrepeats())
        bst = AVLTree(parse(td.str_11)[1])
        self.assertFalse(bst.is_correct_wrepeats())
        bst = AVLTree(parse(td.str_12)[1])
        self.assertTrue(bst.is_correct_wrepeats())
        bst = AVLTree(parse(td.str_13)[1])
        self.assertFalse(bst.is_correct_wrepeats())
        bst = AVLTree(parse(td.str_14)[1])
        self.assertFalse(bst.is_correct_wrepeats())
        bst = AVLTree(parse(td.str_15)[1])
        self.assertFalse(bst.is_correct_wrepeats())
        bst = AVLTree(parse(td.str_16)[1])
        self.assertTrue(bst.is_correct_wrepeats())
        bst = AVLTree(parse(td.str_17)[1])
        self.assertFalse(bst.is_correct_wrepeats())

    def test_calculate_height(self):
        bst = AVLTree(parse(td.str_5)[1])
        bst.calculate_height()
        self.assertEqual(bst.height, 4)
        bst = AVLTree(parse(td.str_6)[1])
        bst.calculate_height()
        self.assertEqual(bst.height, 2)
        bst = AVLTree(parse(td.str_8)[1])
        bst.calculate_height()
        self.assertEqual(bst.height, 1)
        bst = AVLTree(parse(td.str_14)[1])
        bst.calculate_height()
        self.assertEqual(bst.height, 3)

    def test_heights(self):
        bst = AVLTree(parse(td.str_5)[1])
        self.assertEqual(bst.height, 4)
        bst.add(6)
        self.assertEqual(bst.height, 5)
        bst.remove(6)
        self.assertEqual(bst.height, 4)
        bst.remove(3)
        self.assertEqual(bst.height, 3)
        bst = AVLTree(parse(td.str_6)[1])
        bst.add(0)
        self.assertEqual(bst.height, 3)
        bst.add(6.5)
        bst.add(30)
        bst.add(35)
        self.assertEqual(bst.height, 4)
        bst.remove(4)
        self.assertEqual(bst.height, 4)
        bst.remove(2)
        self.assertEqual(bst.height, 4)
        bst.remove(7)
        self.assertEqual(bst.height, 3)
        bst = AVLTree(parse(td.str_8)[1])
        self.assertEqual(bst.height, 1)
        bst = AVLTree(parse(td.str_14)[1])
        self.assertEqual(bst.height, 3)
        avl = AVLTree(Node(10))
        self.assertEqual(avl.height, 0)
        avl.balanced_remove(10)
        self.assertEqual(avl.height, 0)
        avl = AVLTree(Node(10, Node(5, Node(3)), Node(13)))
        left, right = avl.split(8)
        self.assertEqual(left.height, 1)
        self.assertEqual(right.height, 1)
        avl = AVLTree(Node(10, Node(5, Node(3)), Node(13)))
        left, right = avl.split(10)
        self.assertEqual(left.height, 1)
        self.assertEqual(left.root.height, 1)
        self.assertEqual(right.height, 0)
        avl = left.AVLmerge(right)
        self.assertEqual(avl.height, 2)
        left, right = avl.split(13)
        self.assertEqual(left.height, 2)
        self.assertEqual(right.height, 0)
        avl = left.AVLmerge(right)
        left, right = avl.split(3)
        self.assertEqual(left.height, 0)
        self.assertEqual(right.height, 1)
        avl = left.AVLmerge(right)
        left, right = avl.split(0)

    def test_is_balanced(self):
        self.assertTrue(self.bst.is_balanced())
        bst = AVLTree(parse(td.str_5)[1])
        self.assertFalse(bst.is_balanced())
        bst = AVLTree(parse(td.str_1)[1])
        self.assertTrue(bst.is_balanced())
        bst = AVLTree(parse(td.str_2)[1])
        self.assertFalse(bst.is_balanced())
        bst = AVLTree(parse(td.str_3)[1])
        self.assertTrue(bst.is_balanced())
        bst = AVLTree(parse(td.str_6)[1])
        self.assertTrue(bst.is_balanced())
        bst = AVLTree(parse(td.str_7)[1])
        self.assertFalse(bst.is_balanced())
        bst = AVLTree(Node(13, Node(10, Node(2)),
                           Node(15, Node(14), Node(18))))
        self.assertTrue(bst.is_balanced())
        avl = AVLTree(Node(2, Node(1)))
        self.assertTrue(avl.is_balanced())

    def test_rotate_right(self):
        node = Node(3, Node(2, Node(1), Node(2.5)), Node(5))
        bst = AVLTree(node)
        bst.rotate_right(bst.root)
        target_tree = AVLTree(Node(2, Node(1), Node(3, Node(2.5), Node(5))))
        self.assertEqual(bst, target_tree)
        node = Node(3, Node(2, Node(1), Node(2.5)), Node(5))
        new_root = Node(0)
        new_root.set_rc = node
        bst = AVLTree(new_root)
        self.assertTrue(bst.is_correct())
        bst.rotate_right(node)
        target_tree = AVLTree(Node(0, None, Node(2, Node(1),
                                                 Node(3, Node(2.5), Node(5)))))
        self.assertEqual(bst, target_tree)

    def test_rotate_left(self):
        node = Node(10, Node(3), Node(15, Node(12), Node(25)))
        bst = AVLTree(node)
        bst.rotate_left(bst.root)
        target_tree = AVLTree(Node(15, Node(10, Node(3), Node(12)), Node(25)))
        self.assertEqual(bst, target_tree)
        node = Node(10, Node(3), Node(15, Node(12), Node(25)))
        new_root = Node(50)
        new_root.set_lc = node
        bst = AVLTree(new_root)
        self.assertTrue(bst.is_correct())
        bst.rotate_left(node)
        target_tree = AVLTree(Node(50, Node(
            15, Node(10, Node(3), Node(12)), Node(25)), None))
        self.assertEqual(bst, target_tree)

    def test_rotate_left_right(self):
        root = Node(5, Node(3, Node(2),
                            Node(4, Node(3.5), Node(4.5))), Node(7))
        bst = AVLTree(root)
        target_root = Node(4, Node(3, Node(2), Node(3.5)),
                           Node(5, Node(4.5), Node(7)))
        target_tree = AVLTree(target_root)
        bst.rotate_left_right(bst.root)
        self.assertEqual(bst, target_tree)

    def test_rotate_right_left(self):
        root = Node(20, Node(10), Node(30,
                                       Node(25, Node(23), Node(27)), Node(35)))
        bst = AVLTree(root)
        target_root = Node(25, Node(20, Node(10),
                                    Node(23)), Node(30, Node(27), Node(35)))
        target_tree = AVLTree(target_root)
        bst.rotate_right_left(bst.root)
        self.assertEqual(bst, target_tree)

    def test_choose_rotation(self):
        node = Node(3, Node(2, Node(1), Node(2.5)))
        bst = AVLTree(node)
        self.assertEqual(bst.choose_rotation(bst.root).__name__,
                         'rotate_right')
        node = Node(10, Node(3), Node(15, Node(12), Node(25)))
        bst = AVLTree(node)
        self.assertEqual(bst.choose_rotation(bst.root), None)
        bst.remove(3)
        self.assertEqual(bst.choose_rotation(bst.root).__name__,
                         'rotate_left')
        bst.remove(12)
        self.assertEqual(bst.choose_rotation(bst.root).__name__, 'rotate_left')
        bst.add(3)
        bst.add(30)
        self.assertEqual(bst.choose_rotation(bst.root).__name__, 'rotate_left')
        root = Node(5, Node(3, Node(2),
                            Node(4, Node(3.5), Node(4.5))), Node(7))
        bst = AVLTree(root)
        self.assertEqual(bst.choose_rotation(root).__name__,
                         'rotate_left_right')
        root = Node(20, Node(10), Node(30,
                                       Node(25, Node(23), Node(27)), Node(35)))
        bst = AVLTree(root)
        self.assertEqual(bst.choose_rotation(root).__name__,
                         'rotate_right_left')
        bst.remove(10)
        self.assertEqual(bst.choose_rotation(root).__name__,
                         'rotate_right_left')
        bst = AVLTree(parse(td.str_5)[1])
        self.assertEqual(bst.choose_rotation(bst.root).__name__, 'rotate_left')
        root = Node(558718173, Node(555846477, Node(498845550)),
                    Node(568048905))
        avl = AVLTree(root)
        self.assertTrue(avl.is_correct())
        self.assertTrue(avl.is_balanced())
        self.assertIsNone(avl.choose_rotation(avl.root))
        avl.balanced_remove(avl.get_min_node().value)
        root = Node(632079556, Node(604265055,
                                    Node(568048905)), Node(686442273))
        avl = AVLTree(root)

    def test_rotate(self):
        bst = AVLTree(parse(td.str_5)[1])
        bst.rotate(bst.find(3))
        self.assertTrue(bst.is_correct())
        self.assertTrue(bst.is_balanced())

    def test_balanced_add(self):
        node = Node(10)
        bst = AVLTree(node)
        bst.balanced_add(20)
        bst.balanced_add(30)
        self.assertEqual(bst.find(30).parent, Node(20))
        bst.balanced_add(5)
        bst.balanced_add(7)
        self.assertTrue(bst.is_correct())
        self.assertTrue(bst.is_balanced())

    def test_balanced_remove(self):
        bst = AVLTree(Node(10, Node(5), Node(15)))
        bst.balanced_remove(5)
        self.assertEqual(bst, AVLTree(Node(10, None, Node(15))))
        bst = AVLTree(Node(1, Node(0), Node(2, None, Node(3))))
        bst.balanced_remove(0)
        self.assertEqual(bst, AVLTree(Node(2, Node(1), Node(3))))
        bst = AVLTree(Node(10, Node(5, Node(2)),
                           Node(15, Node(13, None, Node(14)), Node(18))))
        self.assertTrue(bst.is_correct())
        self.assertTrue(bst.is_balanced())
        self.assertEqual(bst.remove(5).value, 10)
        self.assertFalse(bst.is_balanced())
        bst.rotate_right_left(bst.root)
        target_tree = AVLTree(Node(13, Node(10, Node(2)),
                                   Node(15, Node(14), Node(18))))
        self.assertEqual(bst, target_tree)
        avl = AVLTree(Node(1))
        avl.balanced_remove(1)
        self.assertEqual(avl, AVLTree())
        root = Node(47253166, Node(21713170),
                    Node(163490772, None, Node(194809808)))
        avl = AVLTree(root)
        avl.balanced_remove(avl.get_max_node().value)
        avl = AVLTree(Node(10, Node(5), Node(15)))
        avl.balanced_remove(10)
        avl.balanced_add(10)

    def test_find_lower_bound(self):
        root = Node(10, Node(5, Node(3, Node(-1), Node(3.5)), Node(7)),
                    Node(20, Node(15, Node(12), Node(18)),
                    Node(25, Node(21, None, Node(22)), Node(30))))
        bst = AVLTree(root)
        self.assertEqual(bst.find_lower_bound(8), Node(10))
        self.assertEqual(bst.find_lower_bound(28), Node(30))
        self.assertEqual(bst.find_lower_bound(35), None)
        self.assertEqual(bst.find_lower_bound(3), Node(3))
        self.assertEqual(bst.find_lower_bound(23), Node(25))

    def test_find_higher_bound(self):
        root = Node(10, Node(5, Node(3, Node(-1), Node(3.5)), Node(7)),
                    Node(20, Node(15, Node(12), Node(18)),
                    Node(25, Node(21, None, Node(22)), Node(30))))
        bst = AVLTree(root)
        self.assertEqual(bst.find_higher_bound(8), Node(7))
        self.assertEqual(bst.find_higher_bound(-1000), None)
        self.assertEqual(bst.find_higher_bound(3), Node(3))
        self.assertEqual(bst.find_higher_bound(2), Node(-1))
        self.assertEqual(bst.find_higher_bound(21.5), Node(21))
        self.assertEqual(bst.find_higher_bound(22.5), Node(22))
        self.assertEqual(bst.find_higher_bound(27), Node(25))
        bst = AVLTree(Node(10, Node(5, None, Node(9)), Node(12)))
        self.assertEqual(bst.find_higher_bound(8), Node(5))

    def test_merge_with_root(self):
        bstl = AVLTree(Node(2, Node(1), Node(3)))
        bstr = AVLTree(Node(6, Node(5), Node(7)))
        root = 4
        self.assertEqual(bstl.merge_with_root(bstr, root),
                         AVLTree(Node(4, Node(2, Node(1), Node(3)),
                                 Node(6, Node(5), Node(7)))))

    def test_merge(self):
        bstl = AVLTree(Node(2, Node(1), Node(3, None, Node(4))))
        bstr = AVLTree(Node(6, Node(5), Node(7)))
        merged = bstl.merge(bstr)
        self.assertEqual(merged,
                         AVLTree(Node(4, Node(2, Node(1), Node(3)),
                                      Node(6, Node(5), Node(7)))))

        self.assertEqual(merged.height, 2)
        self.assertEqual(merged.summ, 28)
        merged = bstl.merge(AVLTree(None))
        self.assertEqual(bstl, merged)
        merged = bstr.merge(AVLTree(None))
        self.assertEqual(bstr, merged)
        merged = AVLTree(None).merge(bstl)
        self.assertEqual(bstl, merged)
        self.assertEqual(AVLTree(None).merge(AVLTree(None)), AVLTree(None))
        bstl = AVLTree(Node(2, Node(1), Node(3, None, Node(4))))
        bst3 = AVLTree(Node(10))
        merged = AVLTree(bstl.merge(bst3).root)
        self.assertTrue(merged.is_balanced())
        self.assertTrue(merged.is_correct)
        AVLBig = AVLTree(Node(4, Node(1, Node(0), Node(3)), Node(8, Node(6))))
        AVLsmall = AVLTree(Node(10))
        merged = AVLTree(AVLBig.merge(AVLsmall).root)
        self.assertTrue(merged.is_correct())

    def test_AVLmerge(self):
        bstl = AVLTree(Node(2, Node(1), Node(3, None, Node(4))))
        bstr = AVLTree(Node(6, Node(5), Node(7)))
        merged = AVLTree(bstl.AVLmerge(bstr).root)
        self.assertEqual(merged, AVLTree(
            Node(4, Node(2, Node(1), Node(3)), Node(6, Node(5), Node(7)))))
        self.assertEqual(merged.summ, 28)
        bstl = AVLTree(Node(2, Node(1), Node(3)))
        bstr = AVLTree(Node(10, Node(5, Node(4)),
                            Node(15, Node(12), Node(20, None, Node(30)))))
        self.assertEqual(bstr.summ, 96)
        self.assertEqual(bstl.summ, 6)
        merged = AVLTree(bstl.AVLmerge(bstr).root)
        self.assertTrue(merged.is_correct())
        self.assertTrue(merged.is_balanced())
        self.assertEqual(merged.height, 3)
        self.assertEqual(merged.summ, 102)
        bstl = AVLTree(Node(2, Node(1), Node(3)))
        bstr = AVLTree(Node(20, Node(10, Node(5, Node(4, Node(3.5)), Node(7)),
                            Node(15, Node(12), Node(17))),
                            Node(30, Node(25, Node(24), Node(27)),
                                 Node(35, Node(32), Node(40)))))
        self.assertTrue(bstr.is_correct)
        self.assertTrue(bstr.is_balanced())

        merged = AVLTree(bstl.AVLmerge(bstr).root)
        self.assertTrue(merged.is_correct())
        self.assertTrue(merged.is_balanced())
        bstr = AVLTree(Node(20, Node(10, Node(5, Node(4, Node(3.5)), Node(7)),
                            Node(15, Node(12), Node(17))),
                            Node(30, Node(25, Node(24), Node(27)),
                                 Node(35, Node(32), Node(40)))))
        self.assertTrue(bstl.is_balanced())
        bstr = AVLTree(Node(100, Node(95), Node(105)))
        merged = AVLTree(bstl.AVLmerge(bstr).root)
        self.assertTrue(merged.is_correct())
        self.assertTrue(merged.is_balanced())
        AVLsmall_left = AVLTree(Node(8))
        AVLsmall_right = AVLTree(Node(10))
        AVLsmall = AVLsmall_left.AVLmerge(AVLsmall_right)
        AVLBig = AVLTree(Node(4, Node(1, Node(0), Node(3)), Node(8, Node(6))))
        AVLsmall = AVLTree(Node(10))
        self.assertEqual(AVLBig.height, 2)
        self.assertEqual(AVLsmall.height, 0)
        merged = AVLTree(AVLBig.AVLmerge(AVLsmall).root)
        self.assertTrue(merged.is_correct())
        self.assertTrue(merged.is_balanced())
        root = Node(5, Node(4), Node(9, Node(7), Node(10)))
        avl = AVLTree(root)
        self.assertEqual(avl, AVLTree().AVLmerge(avl))
        self.assertEqual(avl, avl.AVLmerge(AVLTree()))
        left = AVLTree(Node(2, Node(1)))
        right = AVLTree(Node(7, Node(4, None, Node(5)), Node(8)))
        merged = AVLTree(left.AVLmerge(right).root)
        self.assertTrue(merged.is_correct())
        self.assertTrue(merged.is_balanced())

    def test_split(self):
        bst = AVLTree(Node(2, Node(1), Node(3)))
        bstl, bstr = bst.split(1)
        self.assertEqual(bstl, AVLTree(Node(1)))
        self.assertEqual(bstl.height, 0)
        self.assertEqual(bstl.summ, 1)
        self.assertEqual(bstr, AVLTree(Node(2, None, Node(3))))
        self.assertEqual(bstr.height, 1)
        self.assertEqual(bstr.summ, 5)
        bst = AVLTree(Node(2, Node(1), Node(3)))
        bstl, bstr = bst.split(2)
        self.assertEqual(bstl, AVLTree(Node(2, Node(1))))
        self.assertEqual(bstl.height, 1)
        self.assertEqual(bstl.summ, 3)
        self.assertEqual(bstr, AVLTree(Node(3)))
        self.assertEqual(bstr.height, 0)
        self.assertEqual(bstr.summ, 3)
        avl = AVLTree(Node(3, Node(2, Node(1), Node(2.5)),
                           Node(5, Node(4), Node(6))))
        left, right = avl.split(0)
        avl = AVLTree(Node(1))
        avl.split(2)
        root = Node(
            689365958,
            Node(
                566054224, Node(235664132, Node(47253166, Node(
                    21713170), Node(150982952)), Node(558718173)), Node(
                        632079556, Node(604265055, Node(568048905)), Node(
                            686442273))), Node(868811327, Node(861004046, Node(
                                779397480)), Node(884835051)))
        avl = AVLTree(root)
        self.assertTrue(avl.is_correct())
        self.assertTrue(avl.is_balanced())
        mid, right = avl.split(884835051)

    def test_orders(self):
        node_2 = Node(2, Node(1), Node(3))
        node_4 = Node(4, node_2, Node(5))
        bst = AVLTree(node_4)
        self.assertEqual(bst.pre_order(), [4, 2, 1, 3, 5])
        self.assertEqual(bst.in_order(), [1, 2, 3, 4, 5])
        self.assertEqual(bst.post_order(), [1, 3, 2, 5, 4])
        bst = AVLTree(parse(td.str_1)[1])
        self.assertEqual(bst.in_order(), [1, 2, 3, 4, 5])
        self.assertEqual(bst.pre_order(), [4, 2, 1, 3, 5])
        self.assertEqual(bst.post_order(), [1, 3, 2, 5, 4])
        bst = AVLTree(parse(td.str_2)[1])
        self.assertEqual(bst.in_order(),
                         [50, 70, 80, 30, 90, 40, 0, 20, 10, 60])
        self.assertEqual(bst.pre_order(),
                         [0, 70, 50, 40, 30, 80, 90, 20, 60, 10])
        self.assertEqual(bst.post_order(),
                         [50, 80, 90, 30, 40, 70, 10, 60, 20, 0])

    def test_from_list(self):
        self.assertEqual(AVLTree().from_list([1, 2, 3]),
                         AVLTree(Node(2, Node(1), Node(3))))

    def test_find_closest_common_ancestor(self):
        avl = AVLTree(Node(3, Node(2, Node(1), Node(2.5)),
                           Node(5, Node(4), Node(6))))
        self.assertEqual(
            avl.find_closest_common_ancestor(avl.find(2.5), avl.find(1)),
            Node(2))
        self.assertEqual(
            avl.find_closest_common_ancestor(avl.find(4), avl.find(1)),
            Node(3))
        self.assertEqual(
            avl.find_closest_common_ancestor(avl.find(4), avl.find(5)),
            Node(5))
        self.assertEqual(
            avl.find_closest_common_ancestor(avl.find(5), avl.find(6)),
            Node(5))
        self.assertEqual(
            avl.find_closest_common_ancestor(avl.find(1), avl.find(2)),
            Node(2))
        self.assertEqual(
            avl.find_closest_common_ancestor(avl.find(1), avl.find(2)),
            Node(2))
        self.assertEqual(
            avl.find_closest_common_ancestor(avl.find(1), avl.find(6)),
            Node(3))
        self.assertEqual(
            avl.find_closest_common_ancestor(avl.find(4), avl.find(2)),
            Node(3))

    def test_multiple_adds(self):
        for i in range(10*6):
            lst = []
            avl = AVLTree()
            random_set = set([int(1000*random.random()) for i in range(20)])
            for rn in random_set:
                avl.balanced_add(rn)
                lst.append(rn)
            try:
                assert(len(avl.in_order()) == len(lst))
            except AssertionError:
                print('lengths do not match')
                print(random_set)
            self.assertEqual(len(avl.in_order()), len(lst))


class TestBalancing(unittest.TestCase):
    def test_add_remove(self):
        operations = [
            ('+', 4608), ('+', 6151), ('+', 526), ('+', 4114), ('+', 3093),
            ('+', 2585), ('+', 8226), ('+', 4645), ('+', 8743), ('+', 3626),
            ('+', 1579), ('+', 7729), ('+', 5175), ('+', 1592), ('+', 4664),
            ('+', 4155), ('+', 586), ('+', 590), ('-', 590), ('+', 6229),
            ('+', 1622), ('+', 7791), ('+', 5749), ('+', 5244), ('+', 2689),
            ('+', 7810), ('+', 9349), ('+', 3209)]

        avl = AVLTree()
        for oper, n in operations:
            if oper == '+':
                avl.balanced_add(n)
            elif oper == '-':
                avl.balanced_remove(n)
            copy = deepcopy(avl)

            try:
                avl.find_summ(980, 6773)
            except AssertionError:
                print(f'(broke on {oper}, {n}')
                print('tree before:')
                copy.print_tree()
                mid, right = copy.split(6773)


class ParseSumsTests(unittest.TestCase):
    def test_find_summ_small(self):
        a = AVLTree()
        a.from_list([3, 8, 0, 6, 10, 2, 4, 1])
        self.assertTrue(a.is_correct())
        self.assertTrue(a.is_balanced())
        self.assertEqual(a.find_summ(6, 9), 14)

        a = AVLTree()
        a.from_list([4, 1, 6, 0, 2, 5])
        self.assertEqual(a.find_summ(6, 7), 6)
        a = AVLTree()
        a.from_list([4, 0, 8, 9])
        self.assertEqual(a.find_summ(5, 7), 0)
        a = AVLTree()
        a.from_list([4, 2, 7, 1, 5, 8])

        self.assertEqual(a.find_summ(3, 9), 24)
        a = AVLTree()
        a.from_list([7, 4, 9, 2, 5])
        self.assertEqual(a.find_summ(5, 9), 21)
        self.assertEqual(AVLTree().find_summ(1, 10), 0)
        self.assertEqual(AVLTree(Node(3)).find_summ(3, 10), 3)
        self.assertEqual(AVLTree(Node(3)).find_summ(4, 10), 0)
        self.assertEqual(AVLTree(Node(3)).find_summ(1, 2), 0)
        self.assertEqual(AVLTree(Node(3)).find_summ(3, 3), 3)
        a = AVLTree().from_list([21, 27, 32, 41, 43, 47, 55, 63, 81, 92])
        self.assertEqual(a.find_summ(1, 31), 48)
        a = AVLTree().from_list([8, 11, 12, 20, 25, 51, 62, 71, 78, 88])
        self.assertEqual(
            a.find_summ(43, 83),
            bisect_sum([8, 11, 12, 20, 25, 51, 62, 71, 78, 88], 43, 83))

    def test_find_summ_large(self):

        lst = [
            9730, 9219, 3600, 8730, 8732, 4652, 3644, 5695, 66, 68, 77, 8785,
            605, 8797, 7263, 4206, 6769, 1146, 7807, 138, 4243, 9387, 7342,
            9416, 4820, 8918, 3288, 3313, 2807, 6397, 7935, 256, 1807, 1811,
            1300, 7456, 7469, 5422]
        avl = AVLTree()
        avl.from_list(lst)
        self.assertTrue(avl.is_correct())
        self.assertTrue(avl.is_balanced())
        a = 9199
        b = 10692
        avl.find_summ(a, b)
        mid, right = avl.split(5400)
        self.assertTrue(AVLTree(mid.root).is_balanced())

        big_list = [
            7175, 1034, 8206, 5135, 8204, 41, 1065, 6701, 4156, 5182, 8768,
            6739, 5211, 9331, 1144, 5753, 7289, 3193, 7295, 1688, 7321,
            3738, 8858, 9392, 8892, 2757, 7367, 5323, 8403, 9974, 5882,
            1279, 2817, 9986, 6405, 6416, 9489, 4890, 2330, 9532, 1854,
            4415, 9537, 2882, 321, 2884, 1873]
        avl = AVLTree().from_list(big_list)
        self.assertTrue(avl.is_correct())
        self.assertTrue(avl.is_balanced())
        lb, rb = 248, 10980
        mid, right = avl.split(rb)
        mid, right = AVLTree(mid.root), AVLTree(right.root)
        self.assertTrue(mid.is_balanced())
        self.assertTrue(right.is_balanced())
        self.assertTrue(mid.is_correct())
        self.assertTrue(right.is_correct())
        left, mid = mid.split(lb)
        left, mid = AVLTree(left.root), AVLTree(mid.root)

        self.assertTrue(mid.is_correct())
        self.assertTrue(left.is_correct())
        avl = AVLTree(left.AVLmerge(mid).AVLmerge(right).root)
        self.assertTrue(avl.is_correct())
        self.assertTrue(avl.is_balanced())

        for i in range(10**2):
            random_list = sorted(
                list(set([int(1000*random.random()) for i in range(100)])))
            avl = AVLTree().from_list(random_list)
            lb = random.randint(0, 1000)
            rb = random.randint(0, 1000)
            self.assertEqual(avl.find_summ(lb, rb),
                             bisect_sum(random_list, lb, rb))
        test = 0
        for i in range(10**1):
            test += 1
            print(f'test #{test}')
            avl = AVLTree()
            random_set = set(
                [int(10000*random.random()) for i in range(1000)])
            counter = 1
            added_randoms = []
            operations = []
            for rn in random_set:
                roll = random.random()
                if roll >= 0.2:
                    added_randoms.append(rn)
                    avl.balanced_add(rn)
                    operations.append(('+', rn))
                else:
                    if added_randoms:
                        to_remove = added_randoms.pop()
                        avl.balanced_remove(to_remove)
                        operations.append(('-', to_remove))
                lb = random.randint(0, 11000)
                rb = random.randint(0, 11000)
                self.assertEqual(avl.find_summ(lb, rb),
                                 bisect_sum(sorted(added_randoms), lb, rb))
                counter += 1


if __name__ == '__main__':
    print('tests started')
    unittest.main()
