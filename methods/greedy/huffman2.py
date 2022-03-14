'''
Восстановите строку по её коду и беспрефиксному коду символов.
В первой строке входного файла заданы два целых числа k и l через пробел —
количество различных букв, встречающихся в строке, и размер получившейся
закодированной строки, соответственно. В следующих kk строках записаны коды
букв в формате "letter: code". Ни один код не является префиксом другого.
Буквы могут быть перечислены в любом порядке. В качестве букв могут встречаться
лишь строчные буквы латинского алфавита; каждая из этих букв встречается в
строке хотя бы один раз. Наконец, в последней строке записана закодированная
строка. Исходная строка и коды всех букв непусты. Заданный код таков, что
закодированная строка имеет минимальный возможный размер.

В первой строке выходного файла выведите строку s. Она должна состоять из
строчных букв латинского алфавита. Гарантируется, что длина правильного
ответа не превосходит 10**4   символов.
Sample Input 1:
1 1
a: 0
0
Sample Output 1:
a

Sample Input 2:
4 14
a: 0
b: 10
c: 110
d: 111
01001100100111
Sample Output 2:
abacabad
'''


import sys


num_chars, len_input_string = sys.stdin.readline().strip().split()
code_dict = {}

for line in range(int(num_chars)):
    char, code = sys.stdin.readline().strip().split(': ')
    code_dict[char] = code

coded_message = sys.stdin.readline().strip()
reverse_code_dict = {value: key for key, value in code_dict.items()}
decoded_message = ''
pivot = 0

while pivot < int(len_input_string):
    for key in reverse_code_dict.keys():
        if coded_message.startswith(key, pivot):
            decoded_message += reverse_code_dict[key]
            pivot += len(key)
            continue

print(decoded_message)
