#!/usr/bin/env python3

def uparrow(a, n, b):
    if n == 0:
        return a * b
    if b == 0:
        return 1
    return uparrow(a, n-1, uparrow(a, n, b-1))

def upify(f):
    def upped(b):
        res = 1
        for _ in range(b):
            res = f(res)
        return res
    return upped

def uparrow2(a, n, b):
    f = lambda c: a * c
    for _ in range(n):
        f = upify(f)
    return f(b)

for testcase in [(3, 0, 5), (2, 1, 4), (2, 2, 4), (4, 1, 3), (3, 2, 2), (3, 2, 3), (3, 3, 2)]:
    print(testcase, uparrow(*testcase), uparrow2(*testcase))
