#!/usr/bin/env python3

import argparse
import json
import pathlib
import sys

import paths

def read_json(fn):
    with fn.open() as f:
        return json.load(f)

class Test:
    def __init__(self, name):
        self.name = name
        self.file = paths.top / "testdata" / (f"test_{name}.json")

class Tdata(Test):
    def read(self):
        return read_json(self.file)

    def write(self, examples):
        with self.file.open("w") as f:
            json.dump(examples, f, indent=4, ensure_ascii=False)

    def fixup_file(self, source):
        self.write(list(self.fixup(read_json(source))))

class CheckConsistent(Tdata):
    def check_all(self):
        for example in self.read():
            assert example[1] == self.answer(example[0])

    def fixup(self, examples):
        for example in examples:
            yield (example[0], self.answer(example[0]))
