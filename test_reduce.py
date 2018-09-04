import lterm
import parse
import tdata

def test_reduce():
    for example in testfile.read():
        parsed = [parse.parse_expr(e) for e in example]
        state = parsed[0]
        print(f"Started with: {state}")
        state = state.reduce_once({})
        for next in parsed[1:]:
            print(f"Expected: {next}")
            print(f"Got: {state}")
            assert next.equiv(state)
            state = state.reduce_once({})
        assert state is None

class Tdata(tdata.Tdata):
    def fixup(self, examples):
        for example in examples:
            new  = []
            state = parse.parse_expr(example[0])
            while state is not None:
                new.append(str(state))
                state = state.reduce_once({})
            yield new

testfile = Tdata("test_reduce")

if __name__ == '__main__':
    testfile.main()
