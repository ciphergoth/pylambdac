import lterm
import parse
import tdata

def test_reduce():
    symbols = {"Y": lterm.MagicY("Y")}
    for example in testfile.read():
        state = parse.parse_expr(example[0][0])
        assert state.prefixcode() == example[0][1]
        for next in example:
            print(f"Expected: {next[0]}")
            print(f"Got: {state}")
            assert state.prefixcode() == next[1]
            state = state.reduce_once(symbols)
        assert state is None

class Tdata(tdata.Tdata):
    def fixup(self, examples):
        symbols = {"Y": lterm.MagicY("Y")}
        for example in examples:
            new = []
            expr = parse.parse_expr(example[0][0])
            while True:
                new.append([str(expr), expr.prefixcode()])
                expr = expr.reduce_once(symbols)
                if expr is None:
                    break
            yield new

testfile = Tdata("test_y")

if __name__ == '__main__':
    testfile.main()
