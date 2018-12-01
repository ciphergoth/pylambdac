import importlib

def all_tests():
    return {n: importlib.import_module(f"test_{n}").testinstance
        for n in ['freevar', 'parse', 'reduce', 'varsubst', 'y']}
