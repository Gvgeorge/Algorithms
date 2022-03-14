'''
По данным двум числам 1 ≤ a, b ≤ 2⋅10**9
найдите их наибольший общий делитель.
Sample Input 1:

18 35
Sample Output 1:

1
Sample Input 2:

14159572 63967072
Sample Output 2:

4
'''


def gcd(a: int, b: int) -> int:
    '''
    Greatest common denominator using Euclid's alghoritm
    '''
    if a == 0:
        return b
    if b == 0:
        return a
    if a < b:
        a, b = b, a
    return gcd(a % b, b)


def main():
    a, b = map(int, input().split())
    print(gcd(a, b))


if __name__ == "__main__":
    main()
