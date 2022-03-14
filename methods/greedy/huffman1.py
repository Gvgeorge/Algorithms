'''
По данной непустой строке s длины не более 10**4, состоящей из строчных букв
латинского алфавита, постройте оптимальный беспрефиксный код. В первой строке
выведите количество различных букв k, встречающихся в строке, и размер
получившейся закодированной строки. В следующих k строках запишите коды букв
в формате "letter: code". В последней строке выведите закодированную строку.
Sample Input 1:
a
Sample Output 1:
1 1
a: 0
0

Sample Input 2:
abacabad
Sample Output 2:
4 14
a: 0
b: 10
c: 110
d: 111
01001100100111
'''

import bisect
import sys


class Node:
    def __init__(self, char: str = None, frequency: int = 0,
                 left: 'Node' = None, right: 'Node' = None):
        self.char = char
        self.left = left
        self.right = right
        self.frequency = self.set_frequency(frequency)

    @property
    def is_leaf(self) -> None:
        if self.right is None and self.left is None:
            return True
        return False

    def set_frequency(self, frequency: int = 0):
        if self.is_leaf:
            self.frequency = frequency
        else:
            self.frequency = self.left.frequency + self.right.frequency
        return self.frequency

    def __eq__(self, other):
        return self.frequency == other.frequency

    def __lt__(self, other):
        return self.frequency < other.frequency

    def __str__(self):
        return f'Leaf for the letter {self.char} of frequency {self.frequency}'

    def __repr__(self):
        return f'Leaf for the letter {self.char} of frequency {self.frequency}'


def calculate_huffman_tree(freq_list: list[tuple[str, int]]) -> Node:
    '''
    freq_list: list of two element tuples
    1st element of the tuple - letter (str)
    2nd element of the tuple - times this char is used in the string
    list is sorted by 2nd tuple element descending

    function goes through list and builds a huffman tree
    '''
    leaf_list = [Node(char=node[0], frequency=node[1]) for node in freq_list]
    while len(leaf_list) > 1:
        right = leaf_list.pop()
        left = leaf_list.pop()
        cur_node = Node(left=left, right=right)
        bisect.insort_right(leaf_list, cur_node, key=lambda x: -x.frequency)
    return leaf_list[0]


def calculate_freq_list(input_string: str) -> list[tuple[str, int]]:
    '''
    input_string - string
    returns a list of two element tuples
    1st element of the tuple - char (str)
    2nd element of the tuple - times this char is in the string (int)
    list is ordered by 2nd tuple element desc

    >>>calculate_freq_list('abacabad')
    >>>[('a', 4), ('b', 2), ('c', 1), ('d', 1)]
    '''
    if not input_string:
        return []
    freq_dict = {letter: input_string.count(letter)
                 for letter in input_string.strip()}
    ordered_list = list(sorted(freq_dict.items(), key=lambda t: -t[1]))
    return ordered_list


def _calculate_huffman_codes(tree: Node, bcode: str = '') -> dict:
    '''
    tree - huffman tree (node)
    returns a dict: key - char, value - binary code
    '''
    if tree.is_leaf:
        huffman_dict[tree.char] = bcode
        return huffman_dict

    left_code = bcode + '0'
    _calculate_huffman_codes(tree.left, left_code)
    right_code = bcode + '1'
    _calculate_huffman_codes(tree.right, right_code)

    return huffman_dict


def calculate_huffman_codes(tree: Node):
    if tree.is_leaf:
        return {tree.char: '0'}
    return _calculate_huffman_codes(tree)


def calculate_huffman_string(input_string: str, huffman_dict: dict) -> str:
    '''
    matches the characters of the input string to the codes from the
    given huffman dictionary

    >>>calculate_huffman_string('abacabad',
                                {'a': '0', 'b': '10', 'c': '110', 'd': '111'})
    >>>01001100100111
    '''
    return ''.join([huffman_dict[char] for char in input_string])


def calculate_huffman_dict_from_input_string(input_string: str) -> dict:
    '''
    build a huffman codes dictionary from  a given string

    >>> calculate_huffman_dict_from_input_string('abacabad')
    >>>{'a': '0', 'b': '10', 'c': '110', 'd': '111'}
    '''
    freq_list = calculate_freq_list(input_string)
    tree = calculate_huffman_tree(freq_list)
    codes = calculate_huffman_codes(tree)
    return calculate_huffman_string(input_string, codes)


huffman_dict = {}
input_string = sys.stdin.read().strip()
output_string = calculate_huffman_dict_from_input_string(input_string)
freq_list = calculate_freq_list(input_string)
code_dict = calculate_huffman_codes(calculate_huffman_tree(freq_list))
print(code_dict)
print(len(freq_list), len(output_string))
for in_char, out_char in code_dict.items():
    print(in_char, ': ', out_char, sep='')


print(output_string)
