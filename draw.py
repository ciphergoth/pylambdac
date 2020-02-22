class Grid:
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.grid = [[0 for _ in range(w * 4 + 1)] for _ in range(h * 2 - 1)]

    def drawh(self, r, cstart, cend):
        for i in range(cstart * 4 + 2, cend * 4 + 3):
            self.grid[r * 2][i] = 1

    def drawl(self, r, cstart, cend):
         for i in range(cstart * 4 + 1, cend * 4 + 4):
            self.grid[r * 2][i] = 1

    def drawv(self, rstart, rend, c):
        for i in range(rstart * 2, rend * 2 + 1):
            self.grid[i][c * 4 + 2] = 1

    def yield_lines(self, rstep):
        yield [0 for _ in range(self.w * 4 + 1)]
        for i, l in enumerate(self.grid):
            for _ in range(1 + (rstep -2) * (i % 2)):
                yield l
        yield [0 for _ in range(self.w * 4 + 1)]

    def print(self):
        for l in self.yield_lines(3):
            print("".join(" #"[x] for x in l))

    def writepbm(self, outfile, pbmscale=10):
        rstep = 4
        with outfile.open("w") as f:
            f.write(f"P1\n")
            f.write(f"{pbmscale * (self.w * 4 + 1)} {pbmscale * (self.h * rstep -1)}\n")
            for l in self.yield_lines(rstep):
                for _ in range(pbmscale):
                    f.write(" ".join("01"[x] for x in l for _ in range(pbmscale)))
                    f.write("\n")

def draw_expr(expr):
    h, w = expr.draw_dims[0:2]
    if w == 1:
        h += 1
    grid = Grid(h, w)
    expr.draw(grid, 0, 0, {})
    return grid
