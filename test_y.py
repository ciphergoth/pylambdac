import lterm
import parse

examples = [
    [
        [
            "Y",
            "v Y"
        ],
        [
            "Y",
            "Y"
        ]
    ],
    [
        [
            "Y x",
            "a v Y v x"
        ],
        [
            "Y x",
            "a Y v x"
        ],
        [
            "x (Y x)",
            "a v x a Y v x"
        ]
    ],
    [
        [
            "Y λf Y. foo f Y",
            "a v Y λd λd a a v foo d 1 d 0"
        ],
        [
            "Y λf Y. foo f Y",
            "a Y λd λd a a v foo d 1 d 0"
        ],
        [
            "(λf Y. foo f Y) (Y λf Y. foo f Y)",
            "a λd λd a a v foo d 1 d 0 a Y λd λd a a v foo d 1 d 0"
        ],
        [
            "λY1. foo (Y λf Y. foo f Y) Y1",
            "λd a a v foo a Y λd λd a a v foo d 1 d 0 d 0"
        ]
    ],
    [
        [
            "Y (λf x. x f) foo",
            "a a v Y λd λd a d 0 d 1 v foo"
        ],
        [
            "Y (λf x. x f) foo",
            "a a Y λd λd a d 0 d 1 v foo"
        ],
        [
            "(λf x. x f) (Y λf x. x f) foo",
            "a a λd λd a d 0 d 1 a Y λd λd a d 0 d 1 v foo"
        ],
        [
            "(λx. x (Y λf x. x f)) foo",
            "a λd a d 0 a Y λd λd a d 0 d 1 v foo"
        ],
        [
            "foo (Y λf x. x f)",
            "a v foo a Y λd λd a d 0 d 1"
        ]
    ]
]

def test_reduce():
    symbols = {"Y": lterm.MagicY("Y")}
    for example in examples:
        state = parse.parse_expr(example[0][0])
        assert state.prefixcode() == example[0][1]
        for next in example:
            print(f"Expected: {next[0]}")
            print(f"Got: {state}")
            assert state.prefixcode() == next[1]
            state = state.reduce_once(symbols)
        assert state is None

def main():
    import json
    symbols = {"Y": lterm.MagicY("Y")}
    res = []
    for example in examples:
        new = []
        expr = parse.parse_expr(example[0][0])
        while True:
            new.append([str(expr), expr.prefixcode()])
            expr = expr.reduce_once(symbols)
            if expr is None:
                break
        res.append(new)
    print(json.dumps(res, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    main()
