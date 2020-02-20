#!/usr/bin/env python3

class Lexp:
    pass

class Var(Lexp):
    def __init__(self, d):
        self._d = d
        self.size = (1, 0, 0, 0)

    def draw(self, grid, wo, ho, ll):
        for i in range(ll[-(self._d + 1)] * 4 + 2, ho * 4 + 3):
            grid[i][wo * 4 + 2] = "#"

class Lambda(Lexp):
    def __init__(self, e):
        self._e = e
        s = e.size
        self.size = (s[0], s[1] + 1, s[2], s[3])

    def draw(self, grid, wo, ho, ll):
        for i in range(wo * 4 + 1, (wo + self.size[0] -1) * 4 + 4):
            grid[ho * 4 + 2][i] = "#"
        ll.append(ho)
        self._e.draw(grid, wo, ho + 1, ll)
        ll.pop()

class Apply(Lexp):
    def __init__(self, l, r):
        self._l = l
        self._r = r
        ls = l.size
        rs = r.size
        self.size = (ls[0] + rs[0], max(ls[1], rs[1]) + 1, ls[3], ls[0] + rs[2])

    def draw(self, grid, wo, ho, ll):
        self._l.draw(grid, wo, ho, ll)
        self._r.draw(grid, wo + self._l.size[0], ho, ll)
        l = (wo + self.size[2]) * 4 + 2
        r = (wo + self.size[3]) * 4 + 2
        for i in range((ho + self._l.size[1] -1) * 4 + 2, (ho + self.size[1] -1) * 4 + 3):
            grid[i][l] = "#"
        for i in range((ho + self._r.size[1] -1) * 4 + 2, (ho + self.size[1] -1) * 4 + 3):
            grid[i][r] = "#"
        for i in range(l, r + 1):
            grid[(ho + self.size[1] -1) * 4 + 2][i] = "#"


def gex():
    l = Lambda
    a = Apply
    v = Var
    return l(a(l(a(v(0), v(0))), l(a(v(1), a(v(0), v(0))))))

ex = gex()
w = ex.size[0]
h = ex.size[1]

grid = [[" " for _ in range(w * 4 + 1)] for _ in range(h * 4 + 1)]
ex.draw(grid, 0, 0, [])

for l in grid:
    print("".join(l))
