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

class Term:
    def equiv(self, other):
        if not isinstance(other, Term):
            return False
        return self.prefixcode() == other.prefixcode()

    def _rolllambda(self, l):
        return self

    def prefixcode(self, *, debruijn=True):
        return " ".join(self._prefixcode([] if debruijn else None))

    def __str__(self):
        return "".join(self._str(False, False))

    def __eq__(self, other):
        if not isinstance(other, Term):
            return False
        return self.prefixcode(False) == other.prefixcode(False)

    def __hash__(self):
        return hash(self.prefixcode(False))

    def reduce_once(self, syms):
        return None

    def lambda_subst(self, expr):
        return None

    def variables(self, free):
        return set(self._variables(free))

class Var(Term):
    def __init__(self, name):
        self.name = name

    def _str(self, bracketa, bracketl):
        yield self.name

    def _prefixcode(self, names):
        if names is not None and self.name in names:
            yield "d"
            yield str(names.index(self.name))
        else:
            yield "v"
            yield self.name

    def reduce_once(self, syms):
        # This is safe because it's only called for vars
        # not under a lambda, so we don't have to worry about shadowing.
        return syms.get(self.name, None)

    def var_subst(self, varsubst):
        return varsubst.var_subst(self)

    def _variables(self, free):
        yield self.name

class Apply(Term):
    def __init__(self, a, b):
        self.a = a
        self.b = b

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
        yield "a"
        yield from self.a._prefixcode(names)
        yield from self.b._prefixcode(names)

    def reduce_once(self, syms):
        ls = self.a.lambda_subst(self.b)
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

class Lambda(Term):
    def __init__(self, v, e):
        self.v = v
        self.e = e

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
            yield "λd"
            names.insert(0, self.v)
            yield from self.e._prefixcode(names)
            del names[0]

    def lambda_subst(self, expr):
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

class MagicY(Term):
    def __init__(self, name):
        self.name = name

    def _str(self, bracketa, bracketl):
        yield self.name

    def _prefixcode(self, names):
        yield "Y"

    def _variables(self, free):
        yield self.name

    def lambda_subst(self, expr):
        return Apply(expr, Apply(self, expr))

    def var_subst(self, varsubst):
        assert varsubst.var_subst(self) is self
        return self
