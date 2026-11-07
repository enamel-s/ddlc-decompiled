#!/usr/bin/env python3
"""
Extract the text of DDLC's .rpy scripts to an .xlsx sheet for translation,
and put the translated text back into the scripts.

The sheet layout matches the translation sheets already in use:

    A: (empty)   B: Original   C: (empty)   D: TL   E: TLC   F: Edit   G: Notes

One worksheet per script file, named after the file (e.g. "script-ch0").
Every quoted string in the file becomes one row, in file order, exactly as it
is written in the script (escapes such as \\" and \\n are kept).

Usage:

    # Make a sheet from one or more scripts (or a whole folder).
    python3 tools/ddlc_xlsx.py extract game/script-ch0.rpy -o script.xlsx
    python3 tools/ddlc_xlsx.py extract game -o all-scripts.xlsx

    # Put translations back. Writes the scripts in place unless --out is given.
    python3 tools/ddlc_xlsx.py apply script.xlsx --game game
    python3 tools/ddlc_xlsx.py apply script.xlsx --game game --out translated/game

When applying, the text used for each row is the first non-empty cell of
Edit, TLC, TL (so a checked or edited line wins over the first draft).

Rows are matched to strings by their original English text, in order, not by
row number. A sheet made from a slightly different version of a script (for
example the pre-Ren'Py 8 decompile) still lines up.

Strings that are code rather than text (labels, file names, image names,
colours, audio paths) are never replaced, even if the sheet has a
translation for them. Pass --force to replace them anyway.

Requires openpyxl:  pip install openpyxl
"""

import argparse
import difflib
import glob
import os
import re
import sys

try:
    import openpyxl
    from openpyxl.styles import Alignment, Font
except ImportError:
    sys.exit("This script needs openpyxl. Install it with: pip install openpyxl")


HEADER = [None, "Original", None, "TL", "TLC", "Edit", "Notes"]
COL_ORIGINAL = 2
COL_TL = 4
COL_TLC = 5
COL_EDIT = 6
WIDTHS = {"A": 10, "B": 54.3, "C": 14.3, "D": 54.3, "E": 13, "F": 13, "G": 26.3}


# ---------------------------------------------------------------------------
# Finding the strings in a script.
# ---------------------------------------------------------------------------

class Literal(object):
    """A string literal in a script: text[start:end] is its content."""

    def __init__(self, start, end, quote, line):
        self.start = start
        self.end = end
        self.quote = quote
        self.line = line


def find_literals(text):
    """
    Returns a list of Literal objects for every string literal in `text`,
    in order. Handles ', ", triple quotes, backslash escapes and # comments.
    """

    rv = []
    i = 0
    n = len(text)
    line = 1

    while i < n:
        c = text[i]

        if c == "\n":
            line += 1
            i += 1
            continue

        if c == "#":
            # A comment runs to the end of the line.
            while i < n and text[i] != "\n":
                i += 1
            continue

        if c in "\"'`":
            quote = text[i:i + 3] if text[i:i + 3] == c * 3 else c
            start = i + len(quote)
            j = start
            start_line = line

            while j < n:
                if text[j] == "\\":
                    j += 2
                    continue
                if text.startswith(quote, j):
                    break
                if text[j] == "\n":
                    if len(quote) == 1:
                        # Unterminated single-line string; give up on it.
                        break
                    line += 1
                j += 1

            if j < n and text.startswith(quote, j):
                rv.append(Literal(start, j, quote, start_line))
                i = j + len(quote)
            else:
                i = start
            continue

        i += 1

    return rv


def project_names(game_dir):
    """Labels, screens, images and transforms defined in the project."""

    names = set()
    pattern = re.compile(r"^\s*(?:init\s+-?\d+\s+)?(?:label|screen|image|transform|style)\s+([\w.]+(?:\s+\w+)*)")

    for fn in glob.glob(os.path.join(game_dir, "*.rpy")):
        with open(fn, encoding="utf-8") as f:
            for l in f:
                m = pattern.match(l)
                if m:
                    names.add(m.group(1).strip())
                    names.add(m.group(1).split()[0])

    return names


CODE_RE = re.compile(r"""
    ^\#[0-9a-fA-F]{3,8}$                       # colour
  | ^<.*>                                      # audio spec, <loop 1.0>bgm/1.ogg
  | \.(?:rpy|rpyc|chr|png|jpe?g|webp|ogg|mp3|wav|opus|ttf|otf|txt|html)$
  | ^[\w.\-]*/[\w./\-]*$                       # paths, gui/foo
  | ^\w*_\w*$                                  # identifiers, ch0_kill
  | ^\w+(?:\.\w+)+$                            # dotted names, renpy.music
  | ^(?:mouseup|mousedown|K)_\w+$              # key names
""", re.VERBOSE)


def is_code(s, names):
    s = s.strip()
    if not s:
        return True
    if s in names:
        return True
    return bool(CODE_RE.search(s))


# ---------------------------------------------------------------------------
# Extract.
# ---------------------------------------------------------------------------

def script_files(paths):
    rv = []
    for p in paths:
        if os.path.isdir(p):
            rv.extend(sorted(glob.glob(os.path.join(p, "*.rpy"))))
        else:
            rv.append(p)
    return rv


def sheet_name(fn):
    return os.path.splitext(os.path.basename(fn))[0][:31]


def setup_sheet(ws):
    ws.append(HEADER)
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(wrap_text=True)
    for col, w in WIDTHS.items():
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"


def extract(args):
    files = script_files(args.scripts)
    if not files:
        sys.exit("No .rpy files found.")

    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    for fn in files:
        with open(fn, encoding="utf-8") as f:
            text = f.read()

        ws = wb.create_sheet(sheet_name(fn))
        setup_sheet(ws)

        count = 0
        for lit in find_literals(text):
            s = text[lit.start:lit.end]
            if args.text_only and is_code(s, set()):
                continue
            ws.append([None, s])
            ws.cell(row=ws.max_row, column=COL_ORIGINAL).alignment = Alignment(wrap_text=True)
            count += 1

        print("{}: {} strings".format(fn, count))

    wb.save(args.output)
    print("Wrote", args.output)


# ---------------------------------------------------------------------------
# Apply.
# ---------------------------------------------------------------------------

def cell_text(row, col):
    if len(row) < col:
        return None
    v = row[col - 1]
    if v is None:
        return None
    v = str(v)
    return v if v.strip() else None


def escape_for(quote, s):
    """Makes the translated text safe to put between `quote` quotes."""

    s = s.replace("\r\n", "\n").replace("\r", "\n")

    if len(quote) == 1:
        s = s.replace("\n", "\\n")
        # Escape quote characters that aren't already escaped.
        s = re.sub(r'(?<!\\)((?:\\\\)*)' + re.escape(quote), lambda m: m.group(1) + "\\" + quote, s)
    else:
        s = s.replace(quote, "\\" + quote[0] * 3)

    if s.endswith("\\") and not s.endswith("\\\\"):
        s += "\\"

    return s


TAG_RE = re.compile(r"\[[^\[\]]*\]|\{/?[a-z]+[^{}]*\}")


def check_tags(original, translated):
    """Returns the [variables] and {text tags} missing from the translation."""

    want = sorted(TAG_RE.findall(original))
    have = sorted(TAG_RE.findall(translated))
    return [t for t in want if t not in have]


def apply(args):
    wb = openpyxl.load_workbook(args.sheet)
    names = project_names(args.game)

    total = 0

    for ws in wb.worksheets:
        fn = os.path.join(args.game, ws.title + ".rpy")
        if not os.path.exists(fn):
            print("{}: no file {}, skipping sheet".format(ws.title, fn))
            continue

        with open(fn, encoding="utf-8") as f:
            text = f.read()

        rows = []
        for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 2):
            original = cell_text(row, COL_ORIGINAL)
            if original is None:
                continue
            tl = cell_text(row, COL_EDIT) or cell_text(row, COL_TLC) or cell_text(row, COL_TL)
            rows.append((i, original, tl))

        literals = find_literals(text)
        contents = [text[l.start:l.end] for l in literals]

        matcher = difflib.SequenceMatcher(None, contents, [r[1] for r in rows], autojunk=False)

        replacements = []
        matched_rows = set()
        skipped = 0
        warnings = []

        for tag, a1, a2, b1, b2 in matcher.get_opcodes():
            if tag != "equal":
                continue

            for k in range(a2 - a1):
                lit = literals[a1 + k]
                rownum, original, tl = rows[b1 + k]
                matched_rows.add(rownum)

                if tl is None or tl == original:
                    continue

                if is_code(original, names) and not args.force:
                    skipped += 1
                    warnings.append("  row {} (line {}): skipped code string {!r}".format(rownum, lit.line, original))
                    continue

                missing = check_tags(original, tl)
                if missing:
                    warnings.append("  row {} (line {}): translation is missing {}".format(rownum, lit.line, " ".join(missing)))

                replacements.append((lit, escape_for(lit.quote, tl)))

        for rownum, original, tl in rows:
            if tl and rownum not in matched_rows:
                warnings.append("  row {}: original text not found in {}: {!r}".format(rownum, fn, original[:60]))

        # Replace from the end so earlier offsets stay valid.
        for lit, new in sorted(replacements, key=lambda r: r[0].start, reverse=True):
            text = text[:lit.start] + new + text[lit.end:]

        out = os.path.join(args.out, ws.title + ".rpy") if args.out else fn
        if args.out:
            os.makedirs(args.out, exist_ok=True)

        if not args.dry_run:
            with open(out, "w", encoding="utf-8", newline="") as f:
                f.write(text)

        print("{}: {} lines translated, {} code strings skipped{}".format(
            out, len(replacements), skipped, " (dry run)" if args.dry_run else ""))
        for w in warnings:
            print(w)

        total += len(replacements)

    print("Done:", total, "lines translated.")


def main():
    ap = argparse.ArgumentParser(description="Extract DDLC script text to .xlsx and apply translations back.")
    sub = ap.add_subparsers(dest="command", required=True)

    e = sub.add_parser("extract", help="write the strings of .rpy files to an .xlsx sheet")
    e.add_argument("scripts", nargs="+", help=".rpy files or folders containing them")
    e.add_argument("-o", "--output", default="script.xlsx", help="output .xlsx file (default: script.xlsx)")
    e.add_argument("--text-only", action="store_true", help="leave out strings that look like code (labels, file names, ...)")
    e.set_defaults(func=extract)

    a = sub.add_parser("apply", help="put the translations from an .xlsx sheet back into the scripts")
    a.add_argument("sheet", help="the translated .xlsx file")
    a.add_argument("--game", default="game", help="folder with the .rpy files (default: game)")
    a.add_argument("--out", help="write translated scripts to this folder instead of in place")
    a.add_argument("--force", action="store_true", help="also replace strings that look like code")
    a.add_argument("--dry-run", action="store_true", help="report what would change without writing")
    a.set_defaults(func=apply)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
