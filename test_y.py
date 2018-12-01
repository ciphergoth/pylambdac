import lterm
import parse
import tdata

class Check(tdata.CheckConsistent):
    def answer(self, example):
        symbols = {"Y": lterm.MagicY("Y")}
        new = []
        expr = parse.parse_expr(example)
        while True:
            new.append([str(expr), expr.prefixcode()])
            expr = expr.reduce_once(symbols)
            if expr is None:
                break
        return new

testinstance = Check("test_y")
