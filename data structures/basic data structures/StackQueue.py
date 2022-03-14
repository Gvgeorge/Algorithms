import sys


class StackQueue:
    '''
    A representation of a queue using two stacks
    '''
    def __init__(self):
        self.right_stack = []
        self.left_stack = []

    def push(self, value: int) -> None:
        '''
        Pushes value into the queue
        '''
        if not self.left_stack or value > self.left_stack[-1][1]:
            self.left_stack.append((value, value))
        else:
            self.left_stack.append((value, self.left_stack[-1][1]))

    def _transfer(self) -> None:
        '''
        Helper function puls values from left stack and pushes them
        into right stack
        '''
        while self.left_stack:
            value = self.left_stack.pop()[0]
            if not self.right_stack or value > self.right_stack[-1][1]:
                self.right_stack.append((value, value))
            else:
                self.right_stack.append((value, self.right_stack[-1][1]))

    def pull(self) -> int:
        '''
        Pulls value from the queue
        '''

        if not self.right_stack and not self.left_stack:
            raise IndexError('both stacks are empty')
        if self.right_stack:
            return self.right_stack.pop()
        self._transfer()
        return self.pull()

    @property
    def max_value(self) -> int:
        if not self.left_stack:
            return self.right_stack[-1][1]
        if not self.right_stack:
            return self.left_stack[-1][1]

        return max(self.left_stack[-1][1], self.right_stack[-1][1])


def local_max(lst: list, length: int) -> list:
    '''
    Calculates max values for parts of the list of a given length
    '''
    sq = StackQueue()
    res = []
    for i in range(length):
        sq.push(lst[i])

    res.append(str(sq.max_value))
    sq.pull()
    for j in range(length, len(lst)):
        sq.push(lst[j])
        res.append(str(sq.max_value))
        sq.pull()
    return res


list_length = sys.stdin.readline()
input_list = [int(i) for i in sys.stdin.readline().split()]
qlen = int(sys.stdin.readline())
print(' '.join(local_max(input_list, qlen)))
