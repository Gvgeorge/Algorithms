import sys


class DisjointSet:
    '''
    Implementation of a disjoint set
    we assume that items in this disjoint set will have a size parameter,
    so each set has the sum of sizes of each item
    we track the item with the maximum size
    '''
    def __init__(self, lst: list):
        self.djset = [[i, lst[i]] for i in range(len(lst))]
        self.cur_max_size = max(lst)

    def find(self, idx: int) -> int:
        '''
        finds root of a set
        '''
        parent = idx
        while self.djset[parent][0] != parent:
            parent = self.djset[parent][0]
        while self.djset[idx][0] != idx:
            temp_idx = idx
            idx = self.djset[idx][0]
            self.djset[temp_idx][0] = parent
        return idx

    def union(self, idx_a: int, idx_b: int) -> None:
        '''
        Joins two sets and update the maximum size
        '''
        if idx_a == idx_b:
            return
        idx_a = self.find(idx_a)
        idx_b = self.find(idx_b)
        if idx_a == idx_b:
            return

        self.djset[idx_a][0] = self.djset[idx_b][0]
        self.djset[idx_b][1] += self.djset[idx_a][1]
        self.djset[idx_a][1] = 0
        if self.djset[idx_b][1] > self.cur_max_size:
            self.cur_max_size = self.djset[idx_b][1]

    @property
    def view_set(self):
        return self.djset


inp = sys.stdin.read().split('\n')

db = [int(i) for i in inp[1].split()]
djset = DisjointSet(db)

for line in inp[2:-1]:
    idxs = [int(a) - 1 for a in line.split()]
    djset.union(idxs[0], idxs[1])
    print(djset.cur_max_size)
