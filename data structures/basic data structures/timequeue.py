import sys


class Node:
    def __init__(self, packet: 'Packet',
                 next: 'Node' = None,
                 prev: 'Node' = None):
        self.packet = packet
        self.next = next
        self.prev = prev

    def set_next(self, other: 'Node') -> None:
        self.next = other

    def set_prev(self, other: 'Node') -> None:
        self.prev = other


class Packet:
    def __init__(self, arrival_time: int, duration: int):
        self.arrival_time = arrival_time
        self.duration = duration
        self.start_time = 0
        self.end_time = 0

    def __str__(self):
        return f'Packet: arrival_time \
            {self.arrival_time}, duration {self.duration}'

    def __repr__(self):
        return f'Packet: arrival_time \
            {self.arrival_time}, duration {self.duration}'


class TimeQueue:
    def __init__(self, max_size=None):
        self.max_size = max_size
        self.length = 0
        self.head = None
        self.tail = None

    def has_space(self) -> bool:
        '''
        Checks if queue has enough space to push a new packet.
        '''
        if self.max_size - self.length >= 1:
            return True
        return False

    def push(self, packet_node: Node) -> int:
        while self.head:
            if self.head.packet.end_time <= packet_node.packet.arrival_time:
                self.pull()
            else:
                break

        if not self.has_space():
            return -1

        if not self.head:
            self.head = self.tail = packet_node
            packet_node.packet.start_time = packet_node.packet.arrival_time
            packet_node.packet.end_time = packet_node.packet.start_time + \
                packet_node.packet.duration
        else:
            self.tail.set_prev(packet_node)
            packet_node.set_next(self.tail)
            self.tail = packet_node
            packet_node.packet.start_time = packet_node.next.packet.end_time
            packet_node.packet.end_time = packet_node.packet.start_time + \
                packet_node.packet.duration
        self.length += 1
        return packet_node.packet.start_time

    def pull(self) -> Node:
        if not self.head:
            return 'Queue is empty'
        old_head = self.head
        self.head = self.head.prev
        self.length -= 1
        return old_head


buffer_size, num_packets = sys.stdin.readline().split()
tqueue = TimeQueue(int(buffer_size))

for line in sys.stdin.readlines():
    arrival_time, duration = line.strip().split()
    packet = Packet(int(arrival_time), int(duration))
    node = Node(packet)
    print(tqueue.push(node))
