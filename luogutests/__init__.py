import runpy
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))


def main():
    args = sys.argv[1:]
    if not args:
        runpy.run_path(
            os.path.join(os.path.dirname(__file__), "run_all.py"),
            run_name="__main__",
        )
        return
    mod, rest = args[0], args[1:]
    mod_file = os.path.join(os.path.dirname(__file__), f"{mod}.py")
    if not os.path.exists(mod_file):
        print(f"未知模块: {mod}")
        sys.exit(1)
    sys.argv = [sys.argv[0]] + rest
    runpy.run_path(mod_file, run_name="__main__")
