import sys


def parse(inp):
    target_str, in_text = inp.strip().split('\n')
    return target_str, in_text


def poly_hash(target_str: str, X: int = 263, P: int = 1000000007):
    '''
    Polynomial hash function.
    X - is constant of the polynomial
    P - number of columns of the hashtable
    '''
    hashed = 0
    for idx, char in enumerate(target_str):
        hashed += ord(char) * pow(X, len(target_str) - 1 - idx, P)
    return hashed % P


def rabin_karp(target_str: str,
               in_text: str,
               X: int = 263,
               P: int = 1000000007,
               ):
    '''
    Implementation of Rabin - Karp algorithm
    target_str - string to be searched
    in_text - string in which the search will be performed
    X - is constant of the polynomial
    P - number of columns of the hashtable
    '''
    length = len(target_str)
    last_mult = pow(X, (length-1), P)

    target_str_hash = poly_hash(target_str)
    first_hash = poly_hash(in_text[:length])
    res = []

    if first_hash == target_str_hash and target_str == in_text[:length]:
        res.append(0)
    prev_hash = first_hash
    for idx, _ in enumerate(in_text[:len(in_text)-length+1]):
        slice = in_text[idx:length+idx]
        if idx == 0:
            continue

        next_hash = prev_hash - ord(in_text[idx - 1]) * last_mult
        next_hash = next_hash % P
        next_hash = next_hash * X % P
        next_hash += ord(in_text[idx+length-1]) % P

        prev_hash = next_hash
        if next_hash == target_str_hash and slice == target_str:
            res.append(idx)

    return res


target_str, in_text = parse(sys.stdin.read())
print(' '.join([str(char) for char in rabin_karp(target_str, in_text)]))
