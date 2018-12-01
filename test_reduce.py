import parse
import tdata

class Check(tdata.CheckConsistent):
    def answer(self, example):
        new  = []
        state = parse.parse_expr(example)
        while state is not None:
            new.append(str(state))
            state = state.reduce_once({})
        return new

testinstance = Check("test_reduce")
