#!/usr/bin/env python3

class Grid:
    def __init__(self, h, w):
        self.grid = [[" " for _ in range(w * 4 + 1)] for _ in range(h * 3)]

    def drawh(self, r, cstart, cend):
        for i in range(cstart * 4 + 2, cend * 4 + 3):
            self.grid[r * 3 + 1][i] = "#"

    def drawl(self, r, cstart, cend):
        for i in range(cstart * 4 + 1, cend * 4 + 4):
            self.grid[r * 3 + 1][i] = "#"

    def drawv(self, rstart, rend, c):
        for i in range(rstart * 3 + 1, rend * 3 + 2):
            self.grid[i][c * 4 + 2] = "#"

    def print(self):
        for l in self.grid:
            print("".join(l))

class Lexp:
    pass

class Var(Lexp):
    def __init__(self, d):
        self._d = d
        self.size = (0, 1, 0, 0)

    def draw(self, grid, ro, co, ll):
        grid.drawv(ll[-(self._d + 1)], ro, co)

class Lambda(Lexp):
    def __init__(self, e):
        self._e = e
        s = e.size
        self.size = (s[0] + 1, s[1], s[2], s[3])

    def draw(self, grid, ro, co, ll):
        grid.drawl(ro, co, co + self.size[1] -1)
        ll.append(ro)
        self._e.draw(grid, ro + 1, co, ll)
        ll.pop()

class Apply(Lexp):
    def __init__(self, l, r):
        self._l = l
        self._r = r
        ls = l.size
        rs = r.size
        self.size = (max(ls[0], rs[0]) + 1, ls[1] + rs[1], ls[3], ls[1] + rs[2])

    def draw(self, grid, ro, co, ll):
        self._l.draw(grid, ro, co, ll)
        self._r.draw(grid, ro, co + self._l.size[1], ll)
        grid.drawv(ro + self._l.size[0] -1, ro + self.size[0] -1, co + self.size[2])
        grid.drawh(ro + self.size[0] -1, co + self.size[2], co + self.size[3])
        grid.drawv(ro + self._r.size[0] -1, ro + self.size[0] -1, co + self.size[3])

def gex():
    l = Lambda
    a = Apply
    v = Var
    return l(a(l(a(v(0), v(0))), l(a(v(1), a(v(0), v(0))))))

ex = gex()

grid = Grid(ex.size[0], ex.size[1])
ex.draw(grid, 0, 0, [])
grid.print()
