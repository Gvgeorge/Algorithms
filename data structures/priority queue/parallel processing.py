import math
from typing import Iterable, Any
import sys


class MinHeap:
    '''
    Implementation of minimum heap via list
    '''

    def __init__(self):
        self.heap = []

    def from_iterable(self, lst: Iterable) -> 'MinHeap':
        '''
        Turns iterable into min heap
        '''
        self.heap = lst[:]

        def _from_iterable(idx):

            rc = self.right_child(idx)
            lc = self.left_child(idx)

            if rc:
                _from_iterable(rc)
            if lc:
                _from_iterable(lc)

            self.sift_down(idx)
        return _from_iterable(0)

    def swap(self, a: Any, b: Any) -> None:
        '''
        helper function
        swaps two elements within a heap
        '''
        self.heap[a], self.heap[b] = self.heap[b], self.heap[a]

    def is_leaf(self, idx: int) -> bool:
        '''
        Checks whether given node (idx) is a leaf or not
        '''
        rc = self.right_child(idx)
        lc = self.left_child(idx)
        return False if rc or lc else True

    def sift_up(self, idx: int) -> None:
        '''
        helper function
        pushes value up the tree
        '''
        if self.parent(idx) is None:
            return
        while self.heap[idx] < self.heap[self.parent(idx)]:
            self.swap(idx, self.parent(idx))
            idx = self.parent(idx)
            if not idx:
                break

    def sift_down(self, idx: int) -> None:
        '''
        helper function
        pushes value down the tree
        '''
        while True:
            if not self.left_child(idx) and not self.right_child(idx):
                break
            if self.right_child(idx) and self.left_child(idx):
                min_child = self.min_child(idx)
                if self.heap[idx] < self.heap[min_child]:
                    break
                self.swap(idx, min_child)
                idx = min_child
            elif self.right_child(idx):
                if self.heap[idx] > self.heap[self.right_child(idx)]:
                    self.swap(idx, self.right_child(idx))
                    idx = self.right_child(idx)
                else:
                    break
            elif self.left_child(idx):
                if self.heap[idx] > self.heap[self.left_child(idx)]:
                    self.swap(idx, self.left_child(idx))
                    idx = self.left_child(idx)
                else:
                    break

    def insert(self, item: Any) -> None:
        '''
        Inserts the item into the heap
        '''
        self.heap.append(item)
        self.sift_up(-1)

    def extract_min(self) -> Any:
        '''
        Removes the minimum value of the heap and returns it
        '''
        min_val = self.min_val
        self.swap(0, -1)
        self.heap.pop()
        self.sift_down(0)
        return min_val

    def remove(self, idx: int) -> None:
        '''
        Removes the value of a given idx from the heap
        '''
        self.change_priority(idx, float('-inf'))
        self.extract_min()

    @property
    def min_val(self) -> Any:
        '''
        Returns the minimum value from the heap without removing it
        '''
        if not self.heap:
            return
        return self.heap[0]

    def change_priority(self, idx: int, priority: float) -> None:
        '''
        Changes priority of an item at a given index
        '''
        old_priority = self.heap[idx]
        self.heap[idx] = priority
        if priority > old_priority:
            self.sift_down(idx)
        else:
            self.sift_up(idx)

    def parent(self, idx: int) -> int:
        '''
        Returns the parent of an item at a given index, None if item is root
        '''
        if idx < 0:
            idx = len(self.heap) + idx
        if idx == 0:
            return None
        if idx >= len(self.heap):
            return None
        return math.ceil(idx/2) - 1

    def left_child(self, idx: int) -> int:
        '''
        Returns the left child of an item at a given index,
        None if it doesn't exist
        '''
        if idx < 0:
            idx = len(self.heap) + idx
        if 2 * idx + 1 >= len(self.heap):
            return None
        return 2 * idx + 1

    def right_child(self, idx: int) -> None:
        '''
        Returns the right child of an item at a given index,
        None if it doesn't exist
        '''

        if idx < 0:
            idx = len(self.heap) + idx
        if 2 * idx + 2 >= len(self.heap):
            return None
        return 2 * idx + 2

    def min_child(self, idx: int) -> int:
        '''
        Returns the child with a lower priority of an item at a given index,
        returns left child if right child doesn't exist
        None if it the item is leaf
        '''
        left_child = self.left_child(idx)
        right_child = self.right_child(idx)
        if not left_child:
            return
        elif not right_child:
            return left_child
        left_child_val = self.heap[left_child]
        right_child_val = self.heap[right_child]
        return left_child if left_child_val < right_child_val else right_child

    @property
    def view_heap(self) -> list:
        return self.heap


class ProcessorQueue(MinHeap):
    '''
    Represents a queue of processors, each processor is defined
    by two elemnt tuple first_element: int - time of completion of the tasks
    for this processor, second: int - id.
    Tasks are represented only by its running time
    '''
    def __init__(self, n_proc: int):
        self.q = []
        self.heap = [[0, i] for i in range(n_proc)]

    def add_task(self, task_time: int) -> None:
        '''
        adds the task to the processor from the top of the heap
        '''
        self.q.append((self.min_val[1], self.min_val[0]))
        self.min_val[0] += task_time
        self.update()

    def update(self):
        self.sift_down(0)


def process(tasks: list, n_processors: int) -> list:
    '''
    creates a heap and pushes tasks into it
    returns a list of tuple that shows running time and
    processor id for each task
    '''
    if len(tasks) < n_processors:
        q = ProcessorQueue(len(tasks))
    else:
        q = ProcessorQueue(n_processors)
    for task in tasks:
        q.add_task(task)
    return q.q


n_proc, _ = sys.stdin.readline().split()
n_proc = int(n_proc)
tasks = [int(task) for task in sys.stdin.readline().split()]
res = process(tasks, n_proc)
for proc, time in res:
    print(proc, time)
