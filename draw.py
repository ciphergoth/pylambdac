#!/usr/bin/env python3

class Lexp:
    pass

class Var(Lexp):
    def __init__(self, d):
        self._d = d
        self.size = [1, 0]

    def draw(self, grid, wo, ho, ll):
        for i in range(ll[-(self._d + 1)] * 4 + 2, ho * 4 + 3):
            grid[i][wo * 4 + 2] = "#"

class Lambda(Lexp):
    def __init__(self, e):
        self._e = e
        w, h = e.size
        self.size = [w, h + 1]

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
        wl, hl = l.size
        wr, hr = r.size
        self.size = [wl + wr, max(hl, hr) + 1]

    def draw(self, grid, wo, ho, ll):
        self._l.draw(grid, wo, ho, ll)
        for i in range((ho + self._l.size[1] -1) * 4 + 2, (ho + self.size[1] -1) * 4 + 3):
            grid[i][wo * 4 + 2] = "#"
        self._r.draw(grid, wo + self._l.size[0], ho, ll)
        for i in range((ho + self._r.size[1] -1) * 4 + 2, (ho + self.size[1] -1) * 4 + 3):
            grid[i][(wo + self._l.size[0]) * 4 + 2] = "#"
        for i in range(wo * 4 + 2, (wo + self._l.size[0]) * 4 + 3):
            grid[(ho + self.size[1] -1) * 4 + 2][i] = "#"


def gex():
    l = Lambda
    a = Apply
    v = Var
    return l(a(l(a(v(0), v(0))), l(a(v(1), a(v(0), v(0))))))

ex = gex()
w, h = ex.size

grid = [[" " for _ in range(w * 4 + 1)] for _ in range(h * 4 + 1)]
ex.draw(grid, 0, 0, [])

for l in grid:
    print("".join(l))
