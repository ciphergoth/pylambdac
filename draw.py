import PIL.Image
import PIL.ImageDraw
import PIL.ImageOps

class Grid:
    def __init__(self, rstep, h, w):
        self.rstep = rstep
        self.h = h
        self.w = w
        self.image = PIL.Image.new("1", (w * 4 - 1, (h - 1) * rstep + 1), 1)
        self.draw = PIL.ImageDraw.Draw(self.image)

    def drawh(self, r, cstart, cend):
        self.draw.rectangle(
            ((cstart * 4 + 1, r * self.rstep),
            (cend * 4 + 1, r * self.rstep)), 0)

    def drawl(self, r, cstart, cend):
        self.draw.rectangle(
            ((cstart * 4, r * self.rstep),
            (cend * 4 + 2, r * self.rstep)), 0)

    def drawv(self, rstart, rend, c):
        self.draw.rectangle(
            ((c * 4 + 1, rstart * self.rstep),
            (c * 4 + 1, rend * self.rstep)), 0)

    def print(self):
        for r in range(self.image.height):
            print("".join("# "[self.image.getpixel((c, r))] for c in range(self.image.width)))

    def write_image(self, outfile, factor=10):
        image = PIL.ImageOps.expand(self.image, border=1, fill=1)
        image = PIL.ImageOps.scale(image, factor, resample=PIL.Image.NEAREST)
        image.save(outfile)

def draw_expr(rstep, expr):
    h, w = expr.draw_dims[0:2]
    if w == 1:
        h += 1
    grid = Grid(rstep, h, w)
    expr.draw(grid, 0, 0, {})
    return grid
