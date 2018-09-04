import lark

import lterm
import paths

grammar = (paths.top / "grammar.lark").read_text()
expr_parser = lark.Lark(grammar, start='expr', parser='lalr')
directives_parser = lark.Lark(grammar, start='directives', parser='lalr')

@lark.v_args(inline=True)
class Transformer(lark.Transformer):
    def var(self, v):
        return lterm.Var(v.value)

    def apply(self, a, b):
        return lterm.Apply(a, b)

    def mlambda(self, vars, e):
        res = e
        for v in reversed(vars.children):
            res = lterm.Lambda(v.value, res)
        return res

    def list(self, *args):
        res = lterm.Var("nil")
        for v in reversed(args):
            res = lterm.Apply(lterm.Apply(lterm.Var("cons"), v), res)
        return res

transformer = Transformer()

def parse_expr(expr):
    return transformer.transform(expr_parser.parse(expr))

def parse_directives(expr):
    return transformer.transform(directives_parser.parse(expr))
