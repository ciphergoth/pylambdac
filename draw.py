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
        self._r.draw(grid, wo + self._l.size[0], ho, ll)
        for i in range(wo * 4 + 2, (wo + self.size[0] -1) * 4 + 3):
            grid[(ho + self.size[1] -1) * 4 + 2][i] = "#"


ex = Lambda(Apply(l=Var(0), r=Var(0)))
w, h = ex.size

grid = [[" " for _ in range(w * 4 + 5)] for _ in range(h * 4 + 5)]
ex.draw(grid, 1, 1, [])

for l in grid:
    print("".join(l))
