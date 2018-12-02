import lterm
import parse
import tdata

class Test(tdata.CheckConsistent):
    def answer(self, example):
        symbols = {"Y": lterm.MagicY("Y")}
        new = []
        expr = parse.parse_expr(example)
        while True:
            new.append([str(expr), expr.prefixcode(debruijn=True)])
            expr = expr.reduce_once(symbols)
            if expr is None:
                break
        return new
