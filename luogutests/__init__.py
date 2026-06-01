import runpy
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))


def main():
    runpy.run_path(
        os.path.join(os.path.dirname(__file__), "run_all.py"),
        run_name="__main__",
    )
