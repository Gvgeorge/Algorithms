'''
not using dicts intentionally
'''
import sys


hash = [None for i in range(10**7)]
_ = sys.stdin.readline()
for line in sys.stdin.readlines():
    line = line.split()
    line[1] = int(line[1])
    if line[0] == 'add':
        hash[line[1]-1] = ' '.join(line[2:])
    elif line[0] == 'del':
        hash[line[1]-1] = None
    elif line[0] == 'find':
        if hash[line[1]-1] is None:
            print('not found')
        else:
            print(hash[line[1]-1])
