import sys
from typing import Any


input = sys.stdin.readline()
str_map = {'}': '{', ']': '[', ')': '('}


class Stack:
    '''
    Implementation of stack data structure based on python's list
    '''
    def __init__(self, maxsize=None):
        self.stack = []

    def push(self, item: Any) -> None:
        '''
        Pushes item into the stack
        '''
        self.stack.append(item)

    def pull(self) -> Any:
        '''
        Pulls item from the top of the stack
        '''
        if self.stack == []:
            raise IndexError("Stack is empty")
        self.stack.pop()

    @property
    def top_value(self) -> Any:
        '''
        Returns top value from the stack, doesn't remove it from the stack
        '''
        if self.stack == []:
            raise IndexError("Stack is empty")
        return self.stack[-1]

    def is_empty(self) -> bool:
        '''
        Checks if stack has no items
        '''
        return True if not self.stack else False

    def __str__(self):
        return ' '.join(str(self.stack))


def brackets_match(string: str, str_map: dict) -> str | int:
    '''
    Given a string with brackets and a map that matches opening and
    closing brackets checks if opening brackets match the closing ones.
    '''
    if string == '':
        return 'Success'
    stack = Stack()
    for num, bracket in enumerate(string):
        if bracket not in str_map.keys() and bracket not in str_map.values():
            continue
        if bracket in str_map.values():
            stack.push((num, bracket))
            continue
        if stack.is_empty():
            return num + 1
        elif str_map[bracket] == stack.top_value[1]:
            stack.pull()
        else:
            return num + 1
    return 'Success' if stack.is_empty() else stack.top_value[0] + 1


print(brackets_match(input, str_map))
