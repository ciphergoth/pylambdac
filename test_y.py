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

testfile = Check("test_y")

def test_y():
    testfile.check_all()

if __name__ == '__main__':
    testfile.main()
