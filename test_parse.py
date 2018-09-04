import lterm
import parse
import tdata

class Check(tdata.CheckConsistent):
    def answer(self, s):
        return parse.parse_expr(s).prefixcode(debruijn=False)

testfile = Check("test_parse")

def test_parse():
    testfile.check_all()

if __name__ == '__main__':
    testfile.main()
