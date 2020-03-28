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
    ({"foo": "λx.x x"}, ["foo bar", "(λx.x x) bar", "bar bar"]),
    ({"bar": "λx.x x"}, ["foo bar"]),
]

class Test(tdata.Test):
    def check_all(self):
        for free, slist in examples:
            freemap = {k:parse.parse_expr(v) for k, v in free.items()}
            parsed = [parse.parse_expr(e) for e in slist]
            state = parsed[0]
            #print(f"Started with: {state}")
            state = state.reduce_once(freemap)
            for next in parsed[1:]:
                #print(f"Expected: {next}")
                #print(f"Got: {state}")
                assert next.equiv(state)
                state = state.reduce_once(freemap)
            assert state is None
