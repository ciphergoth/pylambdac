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

PALETTE = ["#BF360C", "#2E7D32", "#4527A0", "#AD1457", "#1565C0", "#827717"]
INK = "#444444"


class MeasureGrid:
    def __init__(self):
        self.binders = []
        self.applies = []

    def drawl(self, r, cstart, cend, name, bid):
        self.binders.append((bid, name))

    def drawv(self, bid, rend, c):
        pass

    def drawfl(self, bot, l_over, cend, aid):
        self.applies.append(aid)

    def drawbl(self, bot, cstart, r_over, aid):
        self.applies.append(aid)

    def drawu(self, bot, l_over, r_over, aid):
        self.applies.append(aid)

    def colours(self):
        ids = [bid for (bid, name) in self.binders] + self.applies
        return {i: PALETTE[n % len(PALETTE)] for (n, i) in enumerate(sorted(ids))}

    def label_margin(self):
        maxlen = max((len(name) for (bid, name) in self.binders), default=0)
        return 0.7 + 0.3 * (1 + maxlen)


class SvgGrid:
    def __init__(self, scale, h, w, colours=None, labels=False, margin=0):
        self.colours = colours
        self.labels = labels
        d = svgwrite.Drawing(size=((w + margin) * scale, h * scale))
        self.dwg = d
        d.add(d.style(
            f"line, polyline {{fill: none; stroke: black; stroke-width: {1/3}px;}}"
            f" text {{font: 0.5px sans-serif; fill: {INK}; text-anchor: end;"
            " paint-order: stroke; stroke: white; stroke-width: 0.15px;"
            " stroke-linejoin: round;}"))
        transform = f"scale({scale}) translate({margin + 0.5} 0.5)"
        self.g = d.add(d.g(transform=transform))
        # Labels go in a later group so lines never paint over them.
        self.lg = d.add(d.g(transform=transform))

    def _style(self, i):
        if self.colours is None:
            return {}
        return {"style": f"stroke: {self.colours[i]};"}

    def _line(self, start, end, i):
        return self.g.add(self.dwg.line(start, end, **self._style(i)))

    def _valueline(self, bid, c, splits, bot):
        # Overdraw the line at c segment by segment: the binder's colour from
        # its lambda down to the first application bar it feeds, then each
        # application's colour from its bar down to the next.
        if self.colours is None:
            return
        rows = [bid[0]] + [r for (r, aid) in splits] + [bot]
        ids = [bid] + [aid for (r, aid) in splits]
        for (i, r0, r1) in zip(ids, rows, rows[1:]):
            self._line((c, r0), (c, r1), i)

    def drawl(self, r, cstart, cend, name, bid):
        l = self._line((cstart - 1/3, r), (cend + 1/3, r), bid)
        l.set_desc(title=name)
        if self.labels:
            self.lg.add(self.dwg.text(f"λ{name}", insert=(cstart - 0.6, r + 0.17)))

    def drawv(self, bid, rend, c):
        self._line((c, bid[0]), (c, rend), bid)

    def drawfl(self, bot, l_over, cend, aid):
        (bid, cstart, splits) = l_over
        self.g.add(self.dwg.polyline([
            (cstart, bid[0]),
            (cstart, bot),
            (cend, bot),
        ], **self._style(aid)))
        self._valueline(bid, cstart, splits, bot)

    def drawbl(self, bot, cstart, r_over, aid):
        (bid, cend, splits) = r_over
        self.g.add(self.dwg.polyline([
            (cstart, bot),
            (cend, bot),
            (cend, bid[0]),
        ], **self._style(aid)))
        self._valueline(bid, cend, splits, bot)

    def drawu(self, bot, l_over, r_over, aid):
        (lbid, cstart, lsplits) = l_over
        (rbid, cend, rsplits) = r_over
        self.g.add(self.dwg.polyline([
            (cstart, lbid[0]),
            (cstart, bot),
            (cend, bot),
            (cend, rbid[0]),
        ], **self._style(aid)))
        self._valueline(lbid, cstart, lsplits, bot)
        self._valueline(rbid, cend, rsplits, bot)

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
