# ddlc-decompiled
Doki Doki Literature Club, decompiled from its .rpa archives and .rpyc files,
and updated to run on the latest Ren'Py 8 (tested against the Ren'Py 8.5
source).

The contents of `images.rpa`, `audio.rpa`, `fonts.rpa` and `scripts.rpa` have
been merged into a normal Ren'Py `game/` folder, so the project can be opened
directly from the Ren'Py launcher.

## Running it

1. Download the Ren'Py 8 SDK from https://www.renpy.org/latest.html.
2. Put this folder in your Ren'Py projects directory (or point the launcher's
   projects directory at the folder that contains it).
3. Select it in the launcher and press "Launch Project".

The game creates a `characters/` folder next to `game/` when it starts, just
like the original release.

## What changed for Ren'Py 8

Ren'Py 8 runs on Python 3, and several engine APIs changed since the
Ren'Py 6.99.12 version DDLC was built with. The main fixes:

- **Layout**: the extracted archives now live in `game/`, matching the paths
  the scripts already use (`images/`, `gui/`, `bgm/`, `sfx/`, `gui/font/`).
- **Character files**: Ren'Py's loader no longer accepts `../` paths, so every
  `renpy.file("../characters/...")` check failed, which sent the game straight
  into the Act 1 ending and Monika's room straight into its ending. These now
  use `character_exists()`, `restore_character()` and `copy_to_basedir()` in
  `definitions.rpy`, which work on the real files with `os`.
- **Python 3**: `global` declared after use in the poem game, `range()` lists
  that are modified (special poems, Monika's topics), `poemwords.txt` read as
  text instead of bytes, and `subprocess` output decoded.
- **Screen effects**: the screen tear and invert effects used a renderer
  `screenshot()` call that no longer exists. They now capture the last frame
  with the current API, upload it to the GPU once, and invert it with
  `InvertMatrix`.
- **Mouse cursor**: `config.mouse` is only read at startup now, so the Act 2
  Sayori-head cursor is registered at init and switched with `default_mouse`.
- **Streamer detection**: uses `tasklist` (`wmic` was removed from Windows 11)
  and falls back to `wmic`.
- **Save locations**: the original removed the `game/saves` location during
  init, but Ren'Py 8 rebuilds the locations after init, so this now happens in
  a start callback.
- **Deprecated APIs**: `LiveComposite` changed to `Composite`, `define
  persistent.*` changed to `default`/init code, mouse warping uses
  `renpy.set_mouse_pos`, and the missing `singleton` module (single-instance
  lock) was removed.
- **Behaviour compatibility**: `options.rpy` keeps two behaviours the scripts
  depend on: layer transforms don't inherit state
  (`config.keep_show_layer_state = False`), and the textbox stays up behind
  choice menus.
