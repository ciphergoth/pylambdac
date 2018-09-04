import lterm
import parse
import tdata

def test_parse():
    for example in testfile.read():
        s = example[0]
        expr = parse.parse_expr(s)
        assert example[1] == expr.prefixcode(debruijn=False)

class Tdata(tdata.Tdata):
    def fixup(self, examples):
        res = []
        for example in examples:
            s = example[0]
            expr = parse.parse_expr(s)
            res.append([s, expr.prefixcode(debruijn=False)])
        return res

testfile = Tdata("test_parse")

if __name__ == '__main__':
    testfile.main()
