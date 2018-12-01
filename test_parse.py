import parse
import tdata

class Check(tdata.CheckConsistent):
    def answer(self, s):
        return parse.parse_expr(s).prefixcode(debruijn=False)

testinstance = Check("test_parse")
