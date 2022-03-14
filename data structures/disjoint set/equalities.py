import sys


class DisjointSet:
    def __init__(self, length: int):
        self.djset = list(range(length))

    def find(self, idx: int) -> int:
        '''
        finds root of a set
        '''
        parent = idx
        while self.djset[parent] != parent:
            parent = self.djset[parent]
        while self.djset[idx] != idx:
            temp_idx = idx
            idx = self.djset[idx]
            self.djset[temp_idx] = parent
        return idx

    def union(self, idx_a: int, idx_b: int) -> None:
        '''
        Joins two sets and update the maximum size
        '''
        if idx_a > idx_b:
            idx_b, idx_a = idx_a, idx_b
        if idx_a == idx_b:
            return
        idx_a = self.find(idx_a)
        idx_b = self.find(idx_b)
        if idx_a == idx_b:
            return

        self.djset[idx_a] = self.djset[idx_b]

    @property
    def view_set(self):
        return self.djset


def parse_input(inp):
    inp = inp.strip().split('\n')
    first_line = [int(i) for i in inp[0].split()]
    comparisons = [i.split() for i in inp[1:]]
    comparisons = [[int(a)-1, int(b)-1] for (a, b) in comparisons]
    n_vars = first_line[0]
    equals = comparisons[:first_line[1]]
    inequals = comparisons[first_line[1]:]
    return (n_vars, equals, inequals)


parsed_input = parse_input(sys.stdin.read())
n_vars = parsed_input[0]
equals = parsed_input[1]
inequals = parsed_input[2]

equals_set = DisjointSet(n_vars)
for eq in equals:
    equals_set.union(eq[0], eq[1])

inequals_set = DisjointSet(n_vars)
for ineq in inequals:
    inequals_set.union(ineq[0], ineq[1])

switch = 1
for a, b in inequals:
    if equals_set.find(a) == equals_set.find(b):
        switch = 0
        break

print(switch)
