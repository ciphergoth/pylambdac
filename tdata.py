#!/usr/bin/env python3

import argparse
import json
import pathlib
import sys

import paths

def read_json(fn):
    with fn.open() as f:
        return json.load(f)

class Tdata:
    def __init__(self, name):
        self.name = name
        self.file = paths.top / "testdata" / (name + ".json")

    def read(self):
        return read_json(self.file)

    def write(self, examples):
        with self.file.open("w") as f:
            json.dump(examples, f, indent=4, ensure_ascii=False)

    def fixup_file(self, source):
        self.write(list(self.fixup(read_json(source))))

    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("sourcefile", type=pathlib.Path)
        args = parser.parse_args()
        self.fixup_file(args.sourcefile)
