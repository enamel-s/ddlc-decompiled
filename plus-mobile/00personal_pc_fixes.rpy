## Fixes for running the DDLC Plus mobile decompile on Windows (or Mac or
## Linux) with Ren'Py 8.5, for personal use. Copy this file into the game/
## folder. It changes nothing on Android, so it can stay in for both builds.
##
## The PC parts of the scripts check the character files and the files next
## to the game with calls like renpy.file("../characters/monika.chr") and
## renpy.file(config.basedir + "/hxppy thxughts.png"). Ren'Py 8 refuses
## "../" in these paths, so every check fails as if the file were missing:
## a new game goes straight to the Act 1 ending, Monika's room ends at once,
## and the desktop's Files app shows no files. This makes renpy.file open
## those paths from disk again, the way older Ren'Py did, so the scripts
## themselves don't need editing.

init -999 python:
    import os

    _ddlc_real_renpy_file = renpy.file

    def _ddlc_file(fn, encoding=None):
        if isinstance(fn, str) and not renpy.mobile:
            name = fn.replace("\\", "/")
            if name.startswith("../") or os.path.isabs(fn):
                # Relative paths are relative to the game/ folder, like the
                # loader. A missing file raises an error, like it used to.
                path = os.path.normpath(os.path.join(config.gamedir, fn))
                if encoding:
                    return open(path, "r", encoding=encoding)
                return open(path, "rb")
        return _ddlc_real_renpy_file(fn, encoding)

    renpy.file = _ddlc_file
