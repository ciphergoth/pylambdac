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
    def __init__(self, rstep, h, w):
        self.rstep = rstep
        self.h = h
        self.w = w
        self.dwg = svgwrite.Drawing(size=((w * 4 - 1, (h - 1) * rstep + 1)),
            fill="black")

    def drawh(self, r, cstart, cend):
        self.dwg.add(self.dwg.rect(
            insert=(cstart * 4 + 1, r * self.rstep),
            size=((cend - cstart) * 4 + 1, 1)))

    def drawl(self, r, cstart, cend):
        self.dwg.add(self.dwg.rect(
            insert=(cstart * 4, r * self.rstep),
            size=((cend - cstart) * 4 + 3, 1)))

    def drawv(self, rstart, rend, c):
        self.dwg.add(self.dwg.rect(
            insert=(c * 4 + 1, rstart * self.rstep),
            size=(1, (rend - rstart) * 4 + 1)))

    def write_image(self, outfile, factor=10):
        self.dwg.saveas(outfile, pretty=True)

def draw_expr(rstep, expr):
    h, w = expr.draw_dims[0:2]
    if w == 1:
        h += 1
    grid = Grid(rstep, h, w)
    expr.draw(grid, 0, 0, {})
    return grid
