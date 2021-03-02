#
# Functions for replacing text data
#

from modules.common import status_print

import glob
import re
import os


def replace_string(prop, expr, before, after):
    """
    Scans the directory for expression and performs a string replacement.

    Params:
    - prop              Properties object or None (for verbosity)
    - expr      (str)   Expression to glob. E.g. *.svg for all SVG files.
                (list)  Alternately, multiple expressions to glob.
    - before    (str)   Hash to change from.
    - after     (str)   Hash to change to.
    """
    def __do_replacement(path, before, after):
        """
        Opens a file in memory, replaces text and saves again.
        """
        if prop:
            status_print(prop, path.replace(prop.target_dir_icons, "").replace(prop.target_dir_theme, ""),
                "'{0}' -> '{1}'".format(before, after))

        newlines = []
        with open(path, "r") as f:
            lines = f.readlines()

        for line in lines:
            newlines.append(re.sub(before, after, line, flags=re.IGNORECASE))

        with open(path, "w") as f:
            f.writelines(newlines)

    expressions = []
    if type(expr) == str:
        expressions.append(expr)
    elif type(expr) == list:
        expressions = expr

    for expr in expressions:
        subpaths = glob.glob("*")
        for subpath in subpaths:
            if os.path.islink(subpath):
                continue

            if not os.path.isdir(subpath):
                if subpath[-11:] == "index.theme":
                    __do_replacement(subpath, before, after)

            if os.path.isdir(subpath):
                files = glob.glob(os.path.join(subpath, "**/" + expr), recursive=True)
                for path in files:
                    if os.path.islink(path):
                        continue

                    if os.path.isfile(path):
                        __do_replacement(path, before, after)
