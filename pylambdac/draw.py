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

import collections
import math

import svgwrite

PALETTE = ["#B01B1B", "#1D4ED8", "#0F7A3D", "#C05717", "#8E24AA", "#0E7490"]
INK = "#444444"


def _oklab(colour):
    rgb = [int(colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    (r, g, b) = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
                 for c in rgb]
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    (l, m, s) = (l ** (1 / 3), m ** (1 / 3), s ** (1 / 3))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def _near():
    # Palette colours closer than this perceptual distance (OKLab x100)
    # count as confusable: the same rules that keep a colour from crossing
    # itself also keep it from crossing these.
    labs = {p: _oklab(p) for p in PALETTE}
    return {p: {q for q in PALETTE
                if 100 * math.dist(labs[p], labs[q]) < 15}
            for p in PALETTE}


NEAR = _near()


def _segments(over, bot):
    # The line for a leftover, split where each application bar it feeds
    # turns it into that application's output: [(id, rstart, rend)].
    (bid, c, splits) = over
    rows = [bid[0]] + [r for (r, aid) in splits] + [bot]
    ids = [bid] + [aid for (r, aid) in splits]
    return list(zip(ids, rows, rows[1:]))


class MeasureGrid:
    def __init__(self):
        self.binders = []
        self.horizontals = []  # (row, cstart, cend, id)
        self.verticals = []  # (col, rstart, rend, id)
        self.attachments = []  # (id, id) meeting at a junction

    def _over(self, over, bot, aid):
        segs = _segments(over, bot)
        for (i, r0, r1) in segs:
            self.verticals.append((over[1], r0, r1, i))
        ids = [i for (i, r0, r1) in segs] + [aid]
        self.attachments.extend(zip(ids, ids[1:]))

    def drawl(self, r, cstart, cend, name, bid):
        self.binders.append((bid, name))
        self.horizontals.append((r, cstart, cend, bid))

    def drawv(self, bid, rend, c):
        self.verticals.append((c, bid[0], rend, bid))

    def drawfl(self, bot, l_over, cend, aid):
        self._over(l_over, bot, aid)
        self.horizontals.append((bot, l_over[1], cend, aid))

    def drawbl(self, bot, cstart, r_over, aid):
        self._over(r_over, bot, aid)
        self.horizontals.append((bot, cstart, r_over[1], aid))

    def drawu(self, bot, l_over, r_over, aid):
        self._over(l_over, bot, aid)
        self._over(r_over, bot, aid)
        self.horizontals.append((bot, l_over[1], r_over[1], aid))

    def colours(self):
        # Greedy graph colouring: things that cross or touch get different
        # colours, and ties go to the least-used colour for variety.
        conflicts = collections.defaultdict(set)

        def clash(a, b):
            if a != b:
                conflicts[a].add(b)
                conflicts[b].add(a)

        for (a, b) in self.attachments:
            clash(a, b)
        for (hr, hc0, hc1, hid) in self.horizontals:
            for (vc, vr0, vr1, vid) in self.verticals:
                if vr0 < hr < vr1 and hc0 <= vc <= hc1:
                    clash(hid, vid)
        counts = {p: 0 for p in PALETTE}
        assigned = {}
        for i in sorted(h[3] for h in self.horizontals):
            used = {assigned[n] for n in conflicts[i] if n in assigned}
            banned = set().union(set(), *(NEAR[p] for p in used))
            free = ([p for p in PALETTE if p not in banned]
                    or [p for p in PALETTE if p not in used] or PALETTE)
            pick = min(free, key=lambda p: (counts[p], PALETTE.index(p)))
            counts[pick] += 1
            assigned[i] = pick
        return assigned

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
            f"line {{fill: none; stroke: black; stroke-width: {1/3}px;}}"
            f" text {{font: 0.5px sans-serif; fill: {INK}; text-anchor: end;"
            " paint-order: stroke; stroke: white; stroke-width: 0.15px;"
            " stroke-linejoin: round;}"))
        transform = f"scale({scale}) translate({margin + 0.5} 0.5)"
        # Layered paint order: horizontals always go over verticals, so
        # lambda lines and bars read as continuous, and labels top both.
        self.vg = d.add(d.g(transform=transform))
        self.hg = d.add(d.g(transform=transform))
        self.lg = d.add(d.g(transform=transform))

    def _line(self, group, start, end, i):
        if self.colours is None:
            return group.add(self.dwg.line(start, end))
        return group.add(self.dwg.line(
            start, end, style=f"stroke: {self.colours[i]};"))

    def _over(self, over, bot):
        for (i, r0, r1) in _segments(over, bot):
            self._line(self.vg, (over[1], r0), (over[1], r1), i)

    def _bar(self, bot, cstart, cend, aid):
        # Extended by half a stroke so it owns the corners with the
        # verticals it meets.
        self._line(self.hg, (cstart - 1/6, bot), (cend + 1/6, bot), aid)

    def drawl(self, r, cstart, cend, name, bid):
        l = self._line(self.hg, (cstart - 1/3, r), (cend + 1/3, r), bid)
        l.set_desc(title=name)
        if self.labels:
            self.lg.add(self.dwg.text(f"λ{name}", insert=(cstart - 0.6, r + 0.17)))

    def drawv(self, bid, rend, c):
        self._line(self.vg, (c, bid[0]), (c, rend), bid)

    def drawfl(self, bot, l_over, cend, aid):
        self._over(l_over, bot)
        self._bar(bot, l_over[1], cend, aid)

    def drawbl(self, bot, cstart, r_over, aid):
        self._over(r_over, bot)
        self._bar(bot, cstart, r_over[1], aid)

    def drawu(self, bot, l_over, r_over, aid):
        self._over(l_over, bot)
        self._over(r_over, bot)
        self._bar(bot, l_over[1], r_over[1], aid)

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
