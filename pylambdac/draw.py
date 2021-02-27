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


class NullGrid:
    def drawl(self, r, cstart, cend, name):
        pass

    def drawv(self, rstart, rend, c):
        pass

    def drawfl(self, rstart, rend, cstart, cend):
        pass

    def drawbl(self, rstart, rend, cstart, cend):
        pass

    def drawu(self, rstart, rend, rback, cstart, cend):
        pass


class SvgGrid:
    def __init__(self, scale, h, w):
        d = svgwrite.Drawing(size=(w * scale, h * scale))
        self.dwg = d
        d.add(d.style(
            f"line, polyline {{fill: none; stroke: black; stroke-width: {1/3}px;}}"))
        self.g = d.add(d.g(transform=f"scale({scale}) translate(0.5 0.5)"))

    def drawl(self, r, cstart, cend, name):
        l = self.g.add(self.dwg.line((cstart - 1/3, r), (cend + 1/3, r)))
        l.set_desc(title=name)

    def drawv(self, rstart, rend, c):
        self.g.add(self.dwg.line((c, rstart), (c, rend)))

    def drawfl(self, rstart, rend, cstart, cend):
        self.g.add(self.dwg.polyline([
            (cstart, rstart),
            (cstart, rend),
            (cend, rend),
        ]))

    def drawbl(self, rstart, rend, cstart, cend):
        self.g.add(self.dwg.polyline([
            (cstart, rend),
            (cend, rend),
            (cend, rstart),
        ]))

    def drawu(self, rstart, rend, rback, cstart, cend):
        self.g.add(self.dwg.polyline([
            (cstart, rstart),
            (cstart, rend),
            (cend, rend),
            (cend, rback),
        ]))

    def write_image(self, outfile):
        self.dwg.saveas(outfile, pretty=True)


def draw_expr(expr, outfile):
    ((h, w), leftover) = expr.draw(NullGrid(), {}, None, 0, 0)
    assert leftover is None
    grid = SvgGrid(40, h, w)
    ((r, c), leftover) = expr.draw(grid, {}, None, 0, 0)
    assert leftover is None
    assert h == r
    assert w == c
    grid.write_image(outfile)
