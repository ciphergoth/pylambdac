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

from pylambdac import parse

from tests import tdata

examples = [
    ("x", {"x"}),
    ("λx. x x", set()),
    ("λx. y x", {"y"}),
]

class Test(tdata.Test):
    def check_all(self):
        for expr, res in examples:
            expr = parse.parse_expr(expr)
            assert res == expr.variables(True)
