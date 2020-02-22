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

def draw_expr(expr):
    grid = Grid(expr.draw_dims[0], expr.draw_dims[1])
    expr.draw(grid, 0, 0, {})
    return grid
