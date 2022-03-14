import unittest
from rope import Node, Rope


class TestNode(unittest.TestCase):
    def setUp(self):
        self.anode = Node('', Node('abc'), Node('def'))

    def test_get_lc(self):
        self.assertEqual(self.anode.left, Node('abc'))

    def test_get_rc(self):
        self.assertEqual(self.anode.right, Node('def'))

    def test_get_value(self):
        self.assertEqual(self.anode.value, '')

    def test_get_parent(self):
        self.assertEqual(self.anode.left.parent, self.anode)

    def test_get_height(self):
        self.assertEqual(Node('abc').height, 0)
        self.assertEqual(self.anode.height, 1)

    def test_get_size(self):
        self.assertEqual(self.anode.size, 6)
        node = Node('')
        self.assertEqual(node.size, 0)
        node = Node('', Node('abc'))
        self.assertEqual(node.size, 3)
        node = Node('', None, Node('', None, Node('', Node('abcd'))))
        self.assertEqual(node.size, 4)

    def test_set_value(self):
        self.anode.set_value = 10
        self.assertEqual(self.anode.value, 10)

    def test_set_lc(self):
        self.anode.set_lc = Node('shortword')
        self.assertEqual(self.anode.left, Node('shortword'))
        self.anode.left.set_lc = Node('q')
        self.assertEqual(self.anode.left.left, Node('q'))

    def test_set_rc(self):
        self.anode.set_rc = Node('join the glorius evolution')
        self.assertEqual(self.anode.right, Node('join the glorius evolution'))
        self.anode.right.set_lc = Node('the time of men has come to an end')
        self.assertEqual(self.anode.right.left,
                         Node('the time of men has come to an end'))

    def test_set_parent(self):
        self.anode.set_parent = Node('3.5')
        self.anode.parent.set_lc = self.anode
        self.assertEqual(self.anode.parent, Node('3.5'))
        self.assertEqual(self.anode.parent.left, self.anode)
        self.assertEqual(self.anode.parent.right, None)

    def test_set_height(self):
        self.anode.set_height = 10
        self.assertEqual(self.anode.height, 10)
        self.anode.update_height()
        self.anode.set_rc = Node('20')
        self.assertEqual(self.anode.height, 1)
        self.anode.right.set_rc = Node('30')
        self.anode.right.update_height()
        self.assertEqual(self.anode.height, 2)
        node = Node('10', Node('5', Node('4'), Node('7')),
                    Node('20', Node('15'), Node('25')))
        self.assertEqual(node.height, 2)
        left = Node('-1', Node('-2', Node('-3')))
        self.assertEqual(left.height, 2)
        node.left.left.set_lc = left
        node.left.left.left.update_height()
        self.assertEqual(node.height, 5)

    def test_size(self):
        self.anode.set_size = 5
        self.assertEqual(self.anode.size, 5)

    def test_comparisons(self):
        self.assertEqual(None, None)
        self.assertNotEqual(Node('3'), None)
        self.assertNotEqual(None, Node('3'))
        self.assertEqual(Node('3'), Node('3'))
        self.assertGreater(Node('4'), Node('3'))
        self.assertGreaterEqual(Node('4'), Node('3'))
        self.assertLessEqual(Node('1'), Node('1'))
        self.assertNotEqual(None, Node(None))
        self.assertTrue(Node('-1'))
        self.assertTrue(Node('0'))

    def test_is_leaf(self):
        self.assertFalse(self.anode.is_leaf())
        self.assertTrue(self.anode.right.is_leaf())


class TestRope(unittest.TestCase):
    def test_swap(self):
        a = Node('a')
        b = Node('b')
        c = Node('c')
        d = Node('d')
        b.set_lc = a
        b.set_rc = c
        rope = Rope(b)
        a.set_lc = d
        rope._swap(a, d)
        self.assertEqual(d.value, 'a')
        self.assertEqual(a.value, 'd')

    def test_remove_node(self):
        a = Node('a')
        b = Node('b')
        c = Node('c')
        b.set_lc = a
        b.set_rc = c
        rope = Rope(b)
        rope.balanced_remove_node(b)
        self.assertEqual(rope, Rope(Node('c', Node('a'))))

        a = Node('a')
        b = Node('b')
        c = Node('c')
        b.set_lc = a
        b.set_rc = c
        rope = Rope(b)
        rope.balanced_remove_node(c)
        self.assertEqual(rope, Rope(Node('b', Node('a'))))

        a = Node('a')
        b = Node('b')
        c = Node('c')
        b.set_lc = a
        b.set_rc = c
        rope = Rope(b)
        rope.balanced_remove_node(a)
        self.assertEqual(rope, Rope(Node('b', None, Node('c'))))

    def test_merge(self):
        root = Node(' ')
        left = Node('e')
        rope = Rope(root)
        left = Rope(left)
        rope = left.merge(rope)
        rope = rope.merge(Rope(Node('g')))
        self.assertEqual(''.join(rope.convert_to_list()), 'e g')

    def test_by_idx(self):
        rope = Rope().convert_from_string('Wealth beyond measure, \
            awarded to the brave and the foolhardy alike.')
        self.assertEqual(rope[0], 'W')
        self.assertEqual(rope[1], 'e')
        self.assertEqual(rope[10], 'o')

    def test_split_by_idx(self):
        rope = Rope().convert_from_string(
            'As the fiend falls, a faint hope blossoms.')
        left, right = rope.split_by_idx(19)
        self.assertEqual(''.join(left.convert_to_list()),
                         'As the fiend falls,')
        self.assertEqual(''.join(right.convert_to_list()),
                         ' a faint hope blossoms.')


if __name__ == '__main__':
    unittest.main()
