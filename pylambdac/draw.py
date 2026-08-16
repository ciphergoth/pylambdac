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

PALETTE = ["#C4552D", "#2E8B6E", "#7C6FDC", "#C33D69", "#3E7CB8", "#A8790B"]
PLUMBING = "#8C8C8C"
INK = "#444444"


class MeasureGrid:
    def __init__(self):
        self.binders = []

    def drawl(self, r, cstart, cend, name, bid):
        self.binders.append((bid, name))

    def drawv(self, bid, rend, c):
        pass

    def drawfl(self, bot, l_over, cend):
        pass

    def drawbl(self, bot, cstart, r_over):
        pass

    def drawu(self, bot, l_over, r_over):
        pass

    def colours(self):
        return {bid: PALETTE[i % len(PALETTE)]
                for (i, (bid, name)) in enumerate(sorted(self.binders))}

    def label_margin(self):
        maxlen = max((len(name) for (bid, name) in self.binders), default=0)
        return 0.7 + 0.3 * (1 + maxlen)


class SvgGrid:
    def __init__(self, scale, h, w, colours=None, labels=False, margin=0):
        self.colours = colours
        self.labels = labels
        d = svgwrite.Drawing(size=((w + margin) * scale, h * scale))
        self.dwg = d
        stroke = "black" if colours is None else PLUMBING
        d.add(d.style(
            f"line, polyline {{fill: none; stroke: {stroke}; stroke-width: {1/3}px;}}"
            f" text {{font: 0.5px sans-serif; fill: {INK}; text-anchor: end;"
            " paint-order: stroke; stroke: white; stroke-width: 0.15px;"
            " stroke-linejoin: round;}"))
        transform = f"scale({scale}) translate({margin + 0.5} 0.5)"
        self.g = d.add(d.g(transform=transform))
        # Labels go in a later group so lines never paint over them.
        self.lg = d.add(d.g(transform=transform))

    def _line(self, start, end, bid):
        if self.colours is None:
            return self.g.add(self.dwg.line(start, end))
        return self.g.add(self.dwg.line(
            start, end, style=f"stroke: {self.colours[bid]};"))

    def _varline(self, bid, c, split, bot):
        # Overdraw the variable's line, from its binder down to where it
        # first feeds an application, in the binder's colour.
        if self.colours is not None:
            self._line((c, bid[0]), (c, bot if split is None else split), bid)

    def drawl(self, r, cstart, cend, name, bid):
        l = self._line((cstart - 1/3, r), (cend + 1/3, r), bid)
        l.set_desc(title=name)
        if self.labels:
            self.lg.add(self.dwg.text(f"λ{name}", insert=(cstart - 0.6, r + 0.17)))

    def drawv(self, bid, rend, c):
        self._line((c, bid[0]), (c, rend), bid)

    def drawfl(self, bot, l_over, cend):
        (bid, cstart, split) = l_over
        self.g.add(self.dwg.polyline([
            (cstart, bid[0]),
            (cstart, bot),
            (cend, bot),
        ]))
        self._varline(bid, cstart, split, bot)

    def drawbl(self, bot, cstart, r_over):
        (bid, cend, split) = r_over
        self.g.add(self.dwg.polyline([
            (cstart, bot),
            (cend, bot),
            (cend, bid[0]),
        ]))
        self._varline(bid, cend, split, bot)

    def drawu(self, bot, l_over, r_over):
        (lbid, cstart, lsplit) = l_over
        (rbid, cend, rsplit) = r_over
        self.g.add(self.dwg.polyline([
            (cstart, lbid[0]),
            (cstart, bot),
            (cend, bot),
            (cend, rbid[0]),
        ]))
        self._varline(lbid, cstart, lsplit, bot)
        self._varline(rbid, cend, rsplit, bot)

    def write_image(self, outfile):
        self.dwg.saveas(outfile, pretty=True)


def draw_expr(expr, outfile, colour=False, labels=False):
    mg = MeasureGrid()
    ((h, w), leftover) = expr.draw(mg, {}, None, 0, 0)
    assert leftover is None
    grid = SvgGrid(40, h, w,
                   mg.colours() if colour else None,
                   labels,
                   mg.label_margin() if labels else 0)
    ((r, c), leftover) = expr.draw(grid, {}, None, 0, 0)
    assert leftover is None
    assert h == r
    assert w == c
    grid.write_image(outfile)
