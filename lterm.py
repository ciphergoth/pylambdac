class Term:
    def equiv(self, other):
        if not isinstance(other, Term):
            return False
        return list(self._prefixcode([])) == list(other._prefixcode([]))

    def _rolllambda(self, l):
        return self

    def prefixcode(self):
        return self._prefixcode(None)

    def __str__(self):
        return self._str(False, False)

    def __eq__(self, other):
        if not isinstance(other, Term):
            return False
        return list(self.prefixcode()) == list(other.prefixcode())

    def __hash__(self):
        return hash(list(self.prefixcode()))

    def reduce_once(self):
        return None

    def lambda_subst(self, expr):
        return None

class Var(Term):
    def __init__(self, name):
        self.name = name

    def _str(self, bracketa, bracketl):
        return self.name

    def _prefixcode(self, names):
        if names is not None and self.name in names:
            yield "d"
            yield str(names.index(self.name))
        else:
            yield "v"
            yield self.name

    def var_subst(self, var, value):
        if self.name == var:
            return value
        else:
            return self

class Apply(Term):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def _str(self, bracketa, bracketl):
        if bracketa:
            return f"({self._str(False, False)})"
        return f"{self.a._str(False, True)} {self.b._str(True, bracketl)}"

    def _prefixcode(self, names):
        yield "a"
        yield from self.a._prefixcode(names)
        yield from self.b._prefixcode(names)

    def reduce_once(self):
        ls = self.a.lambda_subst(self.b)
        if ls is not None:
            return ls
        ra = self.a.reduce_once()
        if ra is not None:
            return Apply(ra, b)
        return None

    def var_subst(self, var, value):
        return Apply(self.a.var_subst(var, value), self.b.var_subst(var, value))

class Lambda(Term):
    def __init__(self, v, e):
        self.v = v
        self.e = e

    def _rolllambda(self, vars):
        vars.append(self.v)
        return self.e._rolllambda(vars)

    def _str(self, bracketa, bracketl):
        if bracketl:
            return f"({self._str(False, False)})"
        vars = []
        e = self._rolllambda(vars)
        return f"λ{' '.join(vars)}. {e._str(False, False)}"

    def _prefixcode(self, names):
        if names is None:
            yield "λ"
            yield self.v
            yield from self.e._prefixcode(None)
        else:
            yield "λd"
            names.insert(0, self.v)
            print(names)
            yield from self.e._prefixcode(names)
            del names[0]

    # FIXME: this is definitely incorrect. Will make correct
    # once I have a failing test to catch the problem.
    def lambda_subst(self, expr):
        return self.e.var_subst(self.v, expr)

    def var_subst(self, var, value):
        return Lambda(self.v, self.e.var_subst(var, value))
