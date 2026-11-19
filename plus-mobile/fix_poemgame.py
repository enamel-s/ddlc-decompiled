#!/usr/bin/env python3
"""
Fixes a Python 3 error in the decompiled script-poemgame.rpy.

The decompiler put each "global" statement after the line that first uses
the variable, which Python 3 refuses to compile. The game only starts now
because the repo ships already-compiled bytecode in game/cache/; once Ren'Py
recompiles the file (after an edit, or with "Force Recompile"), it fails with
"name 'sayoriTime' is used prior to global declaration".

Usage:
    python3 plus-mobile/fix_poemgame.py path/to/DDLC-Plus-Mobile/game

Safe to run more than once.
"""

import os
import re
import sys

if len(sys.argv) != 2:
    sys.exit(__doc__)

path = os.path.join(sys.argv[1], "script-poemgame.rpy")
with open(path, encoding="utf-8") as f:
    text = f.read()

pattern = re.compile(r"^( +)if st > (\w+)Time:\n +global \2Time\n", re.M)
fixed, count = pattern.subn(lambda m: "{0}global {1}Time\n{0}if st > {1}Time:\n".format(m.group(1), m.group(2)), text)

if count:
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(fixed)

print("{}: fixed {} global statement(s).".format(path, count))
