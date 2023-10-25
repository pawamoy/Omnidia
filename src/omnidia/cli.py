# Why does this file exist, and why not put this in `__main__`?
#
# You might be tempted to import things from `__main__` later,
# but that will cause problems: the code will get executed twice:
#
# - When you run `python -m omnidia` python will execute
#   `__main__.py` as a script. That means there won't be any
#   `omnidia.__main__` in `sys.modules`.
# - When you import `__main__` it will get executed again (as a module) because
#   there's no `omnidia.__main__` in `sys.modules`.

"""Module that contains the command line application."""

import argparse
import os
from typing import List, Optional

from omnidia.scanner import scan
from omnidia.watcher import watch

PATH = os.environ.get("NEOWATCH", ".")


def get_parser() -> argparse.ArgumentParser:
    """
    Return the CLI argument parser.

    Returns:
        An argparse parser.
    """
    parser = argparse.ArgumentParser(prog="omnidia")
    parser.add_argument("--scan", action="store_true", default=False)
    parser.add_argument("--watch", action="store_true", default=False)
    parser.add_argument("--path", default=PATH)
    return parser


def main(args: Optional[List[str]] = None) -> int:
    """
    Run the main program.

    This function is executed when you type `omnidia` or `python -m omnidia`.

    Arguments:
        args: Arguments passed from the command line.

    Returns:
        An exit code.
    """
    parser = get_parser()
    opts = parser.parse_args(args=args)
    if opts.scan:
        scan(opts.path)
    if opts.watch:
        watch(opts.path)
    return 0
