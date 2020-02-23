# Copyright 2018 Google LLC
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

import contextlib
import re

def findname(name, forbidden):
    prefix = re.fullmatch(r"(.*\D)?(\d*)", name).group(1)
    if prefix is None: prefix = "_"
    i = 1
    while True:
        newname = f"{prefix}{i}"
        if newname not in forbidden:
            return newname
        i += 1

class VarSubst:
    def __init__(self, var, expr, intarget):
        self.var = var
        self.expr = expr
        freeinsource = expr.variables(True)
        tosubst = freeinsource & intarget
        forbidden = freeinsource | intarget
        self.substplan = {}
        for name in tosubst:
            newname = findname(name, forbidden)
            self.substplan[name] = newname
            forbidden.add(newname)
        # Use presence in subst to track shadowing
        if self.var not in tosubst:
            self.substplan[self.var] = self.var
        self.subst = {}

    @contextlib.contextmanager
    def substitution(self, var):
        if var not in self.substplan:
            yield var
        elif var in self.subst:
            yield self.subst[var]
        else:
            self.subst[var] = self.substplan[var]
            yield self.subst[var]
            del self.subst[var]

    def var_subst(self, var):
        if var.name in self.subst:
            return Var(self.subst[var.name])
        elif var.name == self.var:
            return self.expr
        else:
            return var

class SearchableStack():
    def __init__(self):
        self.s = []

    def push(self, v):
        self.s.append(v)

    def pop(self):
        self.s.pop()

    @contextlib.contextmanager
    def add(self, v):
        self.push(v)
        yield
        self.pop()

    def search(self, sv):
        for i, v in enumerate(reversed(self.s)):
            if v == sv:
                return i
        return None

class Term:
    def equiv(self, other):
        if not isinstance(other, Term):
            return False
        return self.prefixcode(debruijn=True) == other.prefixcode(debruijn=True)

    def _rolllambda(self, l):
        return self

    def prefixcode(self, *, debruijn):
        return " ".join(self._prefixcode(SearchableStack() if debruijn else None))

    def __str__(self):
        return "".join(self._str(False, False))

    def __eq__(self, other):
        if not isinstance(other, Term):
            return False
        return self.prefixcode(debruijn=False) == other.prefixcode(debruijn=False)

    def __hash__(self):
        return hash(self.prefixcode(debruijn=False))

    def reduce_once(self, syms):
        return None

    def lambda_subst(self, expr, syms):
        return None

    def variables(self, free):
        return set(self._variables(free))

    def size(self):
        return self._size(SearchableStack())

class Var(Term):
    def __init__(self, name):
        self.name = name
        self.draw_dims = (0, 1, 0, 0)

    def _str(self, bracketa, bracketl):
        yield self.name

    def _prefixcode(self, names):
        if names is not None:
            position = names.search(self.name)
            if position is not None:
                yield "^"
                yield str(position)
                return
        yield "\'"
        yield self.name

    def reduce_once(self, syms):
        # This is safe because it's only called for vars
        # not under a lambda, so we don't have to worry about shadowing.
        return syms.get(self.name, None)

    def var_subst(self, varsubst):
        return varsubst.var_subst(self)

    def _variables(self, free):
        yield self.name

    def draw(self, grid, ro, co, ll):
        grid.drawv(ll[self.name], ro, co)

    def _size(self, names):
        return 2 + names.search(self.name)

class Apply(Term):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        ls = a.draw_dims
        rs = b.draw_dims
        self.draw_dims = (max(ls[0], rs[0]) + 1, ls[1] + rs[1], ls[3], ls[1] + rs[2])

    def _str(self, bracketa, bracketl):
        if bracketa:
            yield "("
            yield from self._str(False, False)
            yield ")"
        else:
            yield from self.a._str(False, True)
            yield " "
            yield from self.b._str(True, bracketl)

    def _prefixcode(self, names):
        yield "."
        yield from self.a._prefixcode(names)
        yield from self.b._prefixcode(names)

    def reduce_once(self, syms):
        ls = self.a.lambda_subst(self.b, syms)
        if ls is not None:
            return ls
        ra = self.a.reduce_once(syms)
        if ra is not None:
            return Apply(ra, self.b)
        return None

    def var_subst(self, varsubst):
        return Apply(self.a.var_subst(varsubst), self.b.var_subst(varsubst))

    def _variables(self, free):
        yield from self.a._variables(free)
        yield from self.b._variables(free)

    def draw(self, grid, ro, co, ll):
        self.a.draw(grid, ro, co, ll)
        self.b.draw(grid, ro, co + self.a.draw_dims[1], ll)
        grid.drawv(ro + self.a.draw_dims[0] -1, ro + self.draw_dims[0] -1, co + self.draw_dims[2])
        grid.drawh(ro + self.draw_dims[0] -1, co + self.draw_dims[2], co + self.draw_dims[3])
        grid.drawv(ro + self.b.draw_dims[0] -1, ro + self.draw_dims[0] -1, co + self.draw_dims[3])

    def _size(self, names):
        return 2 + self.a._size(names) + self.b._size(names)

class Lambda(Term):
    def __init__(self, v, e):
        self.v = v
        self.e = e
        s = e.draw_dims
        self.draw_dims = (s[0] + 1, s[1], s[2], s[3])

    def _rolllambda(self, vars):
        vars.append(self.v)
        return self.e._rolllambda(vars)

    def _str(self, bracketa, bracketl):
        if bracketl:
            yield "("
            yield from self._str(False, False)
            yield ")"
        else:
            vars = []
            e = self._rolllambda(vars)
            yield  f"λ{' '.join(vars)}. "
            yield from e._str(False, False)

    def _prefixcode(self, names):
        if names is None:
            yield "λ"
            yield self.v
            yield from self.e._prefixcode(None)
        else:
            yield "λ^"
            with names.add(self.v):
                yield from self.e._prefixcode(names)

    def lambda_subst(self, expr, syms):
        forbidden = self.e.variables(False)
        tosubst = VarSubst(self.v, expr, forbidden)
        return self.e.var_subst(tosubst)

    def var_subst(self, varsubst):
        with varsubst.substitution(self.v) as newv:
            return Lambda(newv, self.e.var_subst(varsubst))

    def _variables(self, free):
        if free:
            for v in self.e._variables(free):
                if v != self.v:
                    yield v
        else:
            yield self.v
            yield from self.e._variables(free)

    def draw(self, grid, ro, co, ll):
        grid.drawl(ro, co, co + self.draw_dims[1] -1)
        old = ll.get(self.v, None)
        ll[self.v] = ro
        self.e.draw(grid, ro + 1, co, ll)
        ll[self.v] = old

    def _size(self, names):
        with names.add(self.v):
            return 2 + self.e._size(names)


class Magic(Term):
    def __init__(self, name):
        self.name = name
        # These can't actually be drawn,
        # but we discover that at draw time
        # so just ensure we don't break init-time calculation.
        self.draw_dims = (0, 1, 0, 0)

    def _str(self, bracketa, bracketl):
        yield self.name

    def _prefixcode(self, names):
        if names is not None:
            yield f"^{self.pcode}"
        else:
            yield f"\'{self.pcode}"
            yield self.name

    def _variables(self, free):
        yield self.name

    def var_subst(self, varsubst):
        assert varsubst.var_subst(self) is self
        return self

class MagicY(Magic):
    pcode = 'Y'
    def lambda_subst(self, expr, syms):
        return Apply(expr, Apply(self, expr))

class MagicEager(Magic):
    pcode = 'E'
    def lambda_subst(self, expr, syms):
        rd = expr.reduce_once(syms)
        if rd is None:
            return None
        return Apply(self, rd)

def get_magic(name, type):
    m = {"Y": MagicY, "eager": MagicEager}
    return m[type](name)
