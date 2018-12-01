import parse

import tdata

examples = [
    ({"foo": "λx.x x"}, ["foo bar", "(λx.x x) bar", "bar bar"]),
    ({"bar": "λx.x x"}, ["foo bar"]),
]

class Test(tdata.Test):
    def check_all(self):
        for free, slist in examples:
            freemap = {k:parse.parse_expr(v) for k, v in free.items()}
            parsed = [parse.parse_expr(e) for e in slist]
            state = parsed[0]
            print(f"Started with: {state}")
            state = state.reduce_once(freemap)
            for next in parsed[1:]:
                print(f"Expected: {next}")
                print(f"Got: {state}")
                assert next.equiv(state)
                state = state.reduce_once(freemap)
            assert state is None
