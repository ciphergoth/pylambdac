# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import svgwrite

class Grid:
    def __init__(self, scale, rstep, h, w):
        self.rstep = rstep
        self.h = h
        self.w = w
        size = ((w * 4 + 1) * scale, ((h - 1) * rstep + 3) * scale)
        self.dwg = svgwrite.Drawing(
            size=size,
            fill="black")
        self.g = self.dwg.g(transform=f"scale({scale}) translate(1 1)")
        self.dwg.add(self.g)

    def drawh(self, r, cstart, cend):
        self.g.add(self.dwg.rect(
            insert=(cstart * 4 + 2, r * self.rstep),
            size=((cend - cstart) * 4 - 1, 1)))

    def drawl(self, r, cstart, cend, name):
        rect = self.dwg.rect(
            insert=(cstart * 4, r * self.rstep),
            size=((cend - cstart) * 4 + 3, 1))
        rect.set_desc(title=name)
        self.g.add(rect)

    def drawv(self, rstart, rend, c):
        self.g.add(self.dwg.rect(
            insert=(c * 4 + 1, rstart * self.rstep + 1),
            size=(1, (rend - rstart) * 4)))

    def write_image(self, outfile):
        self.dwg.saveas(outfile, pretty=True)

def draw_expr(rstep, expr):
    h, w = expr.draw_dims[0:2]
    if w == 1:
        h += 1
    grid = Grid(10, rstep, h, w)
    expr.draw(grid, 0, 0, {})
    return grid
