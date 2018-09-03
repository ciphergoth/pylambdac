import lterm
import parse

examples = [
    ("x", {"x"}),
    ("λx. x x", set()),
    ("λx. y x", {"y"}),
]

def test_freevar():
    for expr, res in examples:
        expr = parse.parse_expr(expr)
        assert res == expr.variables(True)
