# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import lark

from pylambdac import lterm
from pylambdac import paths

grammar = (paths.top / "pylambdac/grammar.lark").read_text()
expr_parser = lark.Lark(grammar, start='expr', parser='lalr')
directives_parser = lark.Lark(grammar, start='directives', parser='lalr')

@lark.v_args(inline=True)
class Transformer(lark.Transformer):
    def var(self, v):
        return lterm.Var(v.value)

    def apply(self, a, b):
        return lterm.Apply(a, b)

    def mlambda(self, vars, e):
        res = e
        for v in reversed(vars.children):
            res = lterm.Lambda(v.value, res)
        return res

    def list(self, *args):
        res = lterm.Var("nil")
        for v in reversed(args):
            res = lterm.Apply(lterm.Apply(lterm.Var("cons"), v), res)
        return res

transformer = Transformer()

def parse_expr(expr):
    return transformer.transform(expr_parser.parse(expr))

def parse_directives(expr):
    return transformer.transform(directives_parser.parse(expr))
