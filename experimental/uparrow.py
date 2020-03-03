#!/usr/bin/env python3
# Copyright 2020 Google LLC
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

def uparrow(a, n, b):
    if n == 0:
        return a * b
    if b == 0:
        return 1
    return uparrow(a, n-1, uparrow(a, n, b-1))

def upify(f):
    def upped(b):
        res = 1
        for _ in range(b):
            res = f(res)
        return res
    return upped

def uparrow2(a, n, b):
    f = lambda c: a * c
    for _ in range(n):
        f = upify(f)
    return f(b)

for testcase in [(3, 0, 5), (2, 1, 4), (2, 2, 4), (4, 1, 3), (3, 2, 2), (3, 2, 3), (3, 3, 2)]:
    print(testcase, uparrow(*testcase), uparrow2(*testcase))
