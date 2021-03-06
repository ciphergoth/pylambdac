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

import argparse
import json
import pathlib
import sys

from pylambdac import paths

def read_json(fn):
    with fn.open() as f:
        return json.load(f)

class Test:
    def __init__(self, name):
        self.name = name

class Tdata(Test):
    def file(self):
        return paths.top / "tests/testdata" / (f"test_{self.name}.json")

    def read(self):
        return read_json(self.file())

    def write(self, examples):
        with self.file().open("w") as f:
            json.dump(examples, f, indent=4, ensure_ascii=False)

    def fixup_file(self, source):
        self.write(list(self.fixup(read_json(source))))

class CheckConsistent(Tdata):
    def check_all(self):
        for example in self.read():
            ans = self.answer(example[0])
            if example[1] != ans:
                print("XXXX FAILURE. Expected value:")
                json.dump(example[1], sys.stdout, indent=4, ensure_ascii=False)
                print("XXXX FAILURE. Actual value:")
                json.dump(ans, sys.stdout, indent=4, ensure_ascii=False)
                assert False

    def fixup(self, examples):
        for example in examples:
            yield (example[0], self.answer(example[0]))
