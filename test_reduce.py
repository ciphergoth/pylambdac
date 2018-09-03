import lterm
import parse

examples = [
    [
        "λx. x x",
    ], [
        "(λx y. y x) λz. z z",
        "(λy. y (λz. z z))",
    ], [
        "(λx y. y x λx.x) λz. z z",
        "λy. y (λz. z z) λx.x",
    ],[
        "(λx y. x) λz. z",
        "λy. (λz. z)"
    ], [
        "(λx. x x) λz q1. z q1",
        "(λz q1. z q1) λz q1. z q1",
        "λq1. (λz q1. z q1) q1",
    ], [
        "(λx q q1 q2 q3 q4. x q2) q",
        "λq5 q1 q2 q3 q4. q q2",
    ], [
        "((λx. (λq1. (λq4. (λq2. (λq3. (x q2)))))) q1)",
        "(λq. (λq4. (λq2. (λq3. (q1 q2)))))",
    ], [
        "(λx q1 q. x) q",
        "λq1 q2. q"
    ], [
        "(λr q. r q1) q",
        "λq2. q q1"
    ],
]

def test_reduce():
    for example in examples:
        parsed = [parse.parse_expr(e) for e in example]
        state = parsed[0]
        print(f"Started with: {state}")
        state = state.reduce_once()
        for next in parsed[1:]:
            print(f"Expected: {next}")
            print(f"Got: {state}")
            assert next.equiv(state)
            state = state.reduce_once()
        assert state is None
