import sys
from typing import Any


P = 1000000007
X = 263


class Node:
    def __init__(self, val, next: 'Node' = None):
        self._val = val
        self._next = next

    @property
    def next(self):
        return self._next

    @property
    def value(self):
        return self._val

    @value.setter
    def set_value(self, val):
        self._val = val

    @next.setter
    def set_next(self, next: 'Node'):
        self._next = next

    def __eq__(self, other: 'Node'):
        if isinstance(other, Node):
            return self.value == other.value
        if other is None:
            return self.value is None

    def __str__(self):
        return f'Node of value {self.value}'

    def __repr__(self):
        return f'Node of value {self.value}'


class LinkedList:
    def __init__(self, root: 'Node'):
        self._root = root
        self._tail = root

    @property
    def root(self):
        return self._root

    @property
    def tail(self):
        return self._tail

    def is_empty(self):
        if self._root is None:
            return True
        return False

    def add(self, node: Node):
        '''
        adds item to the beginning
        '''
        if self._root == Node(None):
            self._root = node
        else:
            node.set_next = self._root
            self._root = node

    def append(self, node: Node):
        '''
        adds item to the end
        '''
        self._tail.set_next = node
        self._tail = node

    def _find(self, item: Any) -> tuple[Node, Node]:
        '''
        finds the item (item is not a node but its value)
        returns a tuple of node with the item and node
        before it
        '''
        if self._root.value == item:
            return (self._root, None)
        pointer = self._root
        prev = None
        while True:
            if pointer.value == item:
                break
            prev = pointer
            pointer = pointer.next
            if pointer is None:
                break
        if pointer is None:
            return (None, None)
        return (pointer, prev)

    def find(self, item: Any) -> Node:
        return self._find(item)[0]

    def remove(self, item: Any) -> None:
        item, prev = self._find(item)
        if item is not None:
            if item.next is None and prev is None:
                self._root = self._tail = Node(None)
            elif prev is None:
                self._root = item.next
            elif item.next is None:
                self._tail = prev
                self._tail.set_next = None
            else:
                prev.set_next = item.next
            del(item)

    def to_list(self) -> list:
        '''
        returns a list with all the values in linked list
        '''
        res = []
        if self._root:
            pointer = self._root
            while pointer:
                cur_val = pointer.value
                res.append(cur_val)
                pointer = pointer.next
        if res == [None]:
            res = []
        return res


class HashTable:
    def __init__(self, length: int, hash_func: callable):
        '''
        hashtable using linked lists
        '''
        self.length = length
        self.table = [LinkedList(Node(None)) for i in range(length)]
        self.hash_func = hash_func

    def get_pos(self, item):
        '''
        calculates hash which is the index for the main list
        '''
        return self.hash_funcc(item, self.length)

    def add(self, item):
        pos = self.get_pos(item)
        exists = self.find(item)
        if not exists:
            self.table[pos].add(Node(item))

    def delete(self, item):
        pos = self.get_pos(item)
        self.table[pos].remove(item)

    def find(self, item):
        pos = self.get_pos(item)
        return False if self.table[pos].find(item) is None else True

    def to_list(self, idx: int):
        '''
        converts a column at a given idx to a list
        '''
        return self.table[idx].to_list()


def hash_funcc(string: str, length: int) -> int:
    '''
    Calculates hash value (int range(0 to length)  of a given string
    '''
    res = 0
    for i in range(len(string)):
        char = ord(string[i])
        res += (char*(X**i))
    res = res % P
    res = res % length
    return res


def parse(string: str) -> tuple:
    string_list = [i.strip() for i in string.strip().split('\n')]
    length = int(string_list[0])
    actions = [i.split() for i in string_list[2:]]
    return length, actions


inp = sys.stdin.read()
m, actions = parse(inp)
hashtable = HashTable(m)
for action, item in actions:
    if action == 'add':
        hashtable.add(item)
    elif action == 'find':
        found = hashtable.find(item)
        if found:
            print('yes')
        else:
            print('no')
    elif action == 'del':
        hashtable.delete(item)
    elif action == 'check':
        print(' '.join(hashtable.to_list(int(item))))
