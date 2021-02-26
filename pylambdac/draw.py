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
            f" line, polyline {{fill: none; stroke: black; stroke-width: {1/3}px; stroke-linejoin: round}}"
            " .lrb {fill: white}"
            " .lr {fill: black}"
        ))
        self.topg = d.add(d.g(transform=f"scale({scale}) translate(0.5 0.5)"))
        self.layers = []
        # self.textg = topg.add(d.g(font_family="Verdana", font_size="0.5", fill="#777", stroke="none"))

    def get_layer(self, r):
        while len(self.layers) <= r:
            self.layers.append((self.topg.add(self.dwg.g()),
                                self.topg.add(self.dwg.g())))
        return self.layers[r]

    def drawl(self, r, cstart, cend, name):
        lg, g = self.get_layer(r)
        lg.add(self.dwg.rect((cstart - 1/3, r - 0.2),
                             (cend - cstart + 2/3, 0.4), class_="lrb"))
        l = lg.add(self.dwg.rect((cstart - 1/3, r - 1/6),
                                 (cend - cstart + 2/3, 1/3), class_="lr"))
        l.set_desc(title=name)
        # self.textg.add(self.dwg.text(name, insert=((cstart + cend)/2, r),
        #    dominant_baseline="middle", text_anchor="middle"))

    def drawv(self, rstart, rend, c):
        lg, g = self.get_layer(rstart)
        g.add(self.dwg.line((c, rstart), (c, rend)))

    def drawfl(self, rstart, rend, cstart, cend):
        lg, g = self.get_layer(rstart)
        g.add(self.dwg.polyline([
            (cstart, rstart),
            (cstart, rend),
            (cend, rend),
        ]))

    def drawbl(self, rstart, rend, cstart, cend):
        lg, g = self.get_layer(rstart)
        g.add(self.dwg.polyline([
            (cstart, rend),
            (cend, rend),
            (cend, rstart),
        ]))

    def drawu(self, rstart, rend, rback, cstart, cend):
        self.drawfl(rstart, rend, cstart, cend)
        self.drawbl(rback, rend, cstart, cend)
        return

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
