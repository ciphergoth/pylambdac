import parse
import tdata

class Test(tdata.CheckConsistent):
    def answer(self, s):
        return parse.parse_expr(s).prefixcode(debruijn=False)
