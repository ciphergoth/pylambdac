import parse

examples = [
    ("x", {"x"}),
    ("λx. x x", set()),
    ("λx. y x", {"y"}),
]

class Test:
    def check_all(self):
        for expr, res in examples:
            expr = parse.parse_expr(expr)
            assert res == expr.variables(True)

testinstance = Test()
