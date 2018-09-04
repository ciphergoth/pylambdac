import lterm
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

testfile = Check("test_reduce")

def test_reduce():
    testfile.check_all()

if __name__ == '__main__':
    testfile.main()
