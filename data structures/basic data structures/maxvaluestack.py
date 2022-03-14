import sys


num_lines = sys.stdin.readline()
max_num = float('-inf')
stack = []
for line in sys.stdin.readlines():
    command = line.strip().split()[0]
    if command == 'push':
        cur_num = int(line.strip().split()[1])
        if not stack:
            stack.append((cur_num, cur_num))
            max_num = cur_num
        elif max_num < cur_num:
            stack.append((cur_num, cur_num))
            max_num = cur_num
        else:
            stack.append((cur_num, max_num))
    if command == 'pop':
        stack.pop()
        max_num = stack[-1][1]
    if command == 'max':
        print(max_num)
