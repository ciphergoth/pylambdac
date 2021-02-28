from pylambdac import draw
from pylambdac import lterm

def flatten_symbols(name, symbols):
    expr = symbols[name]
    while True:
        free = expr.variables(True)
        if not free:
            #print(f"flat: {expr}")
            return expr
        #print(f"flattening {expr}")
        subst = None
        for p in symbols.items():
            if p[0] in free:
                subst = p
        if subst == None:
            print(f"Defies flattening: {expr}")
            print(f"Free variables: {free}")
            return None
        if subst[0] in subst[1].variables(True):
            print(f"Recursive: {expr}")
            return None
        #print(f"substituting {subst[0]} = {subst[1]}")
        expr = lterm.Apply(lterm.Lambda(subst[0], expr), subst[1])

def optimize(expr):
    while True:
        newexpr = expr.optimize()
        if newexpr is None:
            return expr
        expr = newexpr
        print(f"optimized: {expr}")

def reduce(expr, symbols):
    while True:
        print("    ", expr)
        next = expr.reduce_once(symbols)
        if next is None:
            return expr
        expr = next

class Processor:
    def __init__(self, args):
        self._args = args
        self._symbols = {}
        self.drawings = []

    def do_let(self, name, value):
        print(f"let {name.value} = {value}")
        assert name.value not in self._symbols
        self._symbols[name.value] = value

    def do_magic(self, name):
        print(f"magic {name.value}")
        assert name.value not in self._symbols
        self._symbols[name.value] = lterm.get_magic(name.value)

    def do_reduce(self, expr):
        print(f"reduce {expr}")
        reduce(expr, self._symbols)
        print()

    def do_asserteq(self, l, r):
        print(f"asserteq ({l}) ({r})")
        l = reduce(l, self._symbols)
        print()
        r = reduce(r, self._symbols)
        print()
        assert l.equiv(r)

    def do_draw(self, name):
        if self._args.outdir is None:
            print(f"draw {name} # no --outdir specified, not drawing")
            return
        print(f"draw {name}")
        expr = flatten_symbols(name, self._symbols)
        if expr is None:
            return
        print(f"flattened: {expr}")
        expr = optimize(expr)
        self._args.outdir.mkdir(parents=True, exist_ok=True)
        target = f"{name}.svg"
        draw.draw_expr(expr, self._args.outdir / target)
        print(f"Expression of {expr.size()} BLC bits saved to {target}")
        self.drawings.append(target)

    def process(self, directives):
        for directive in directives.children:
            getattr(self, f"do_{directive.data}")(*directive.children)
