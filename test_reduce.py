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
        "(λy. y (λz. z z) λx.x)",
    ],[
        "((λx. (λy. x)) (λz. z))",
        "(λy. (λz. z))"
    ], [
        "((λx. (λy. (x x))) (λz. (λq1. (z q1))))",
        "(λy. ((λz. (λq1. (z q1))) (λz. (λq1. (z q1)))))",
        "(λy. (λq1. ((λz. (λq1. (z q1))) q1)))",
        "(λy. (λq1. (λq. (q1 q))))",
    ], [
        "(λq. ((λx. (λq. (λq1. (λq2. (λq3. (λq4. (x q2))))))) q))",
        "(λq. (λq1. (λq2. (λq3. (λq4. (λq5. (q q3)))))))",
    ], [
        "(λq1. ((λx. (λq1. (λq4. (λq2. (λq3. (x q2)))))) q1))",
        "(λq1. (λq. (λq4. (λq2. (λq3. (q1 q2))))))",
    ], [
        "λq. (λx q1 q. x) q",
        "λq q1 q2. q"
    ], [
        "λq q1. (λr q. r q1) q",
        "λq q1. λq2. q q1"
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
