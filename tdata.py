#!/usr/bin/env python3

import argparse
import json
import pathlib
import sys

import paths

class Tdata:
    def __init__(self, name):
        self.name = name
        self.file = paths.top / "testdata" / (name + ".json")

    def read(self):
        with self.file.open() as f:
            return json.load(f)

    def fixup_file(self, source):
        with source.open() as f:
            examples = json.load(f)
        examples = self.fixup(examples)
        with self.file.open("w") as f:
            json.dump(examples, f, indent=4, ensure_ascii=False)

    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("sourcefile", type=pathlib.Path)
        args = parser.parse_args()
        self.fixup_file(args.sourcefile)
