# Personal Burmese build of the DDLC mobile decompile

Files for building the base DDLC game from the
[HiroStuff/DDLC-Plus-Mobile](https://github.com/HiroStuff/DDLC-Plus-Mobile)
decompile in Burmese, for your own phone. Nothing from that repo is included
here. These are only the extra files you copy into your own checkout of it.

The Plus content (side stories, gallery, music, mail) isn't touched. It stays
locked behind its purchase screen, and purchases don't work in a personal
build.

Keep the APK to yourself: it contains the whole game.

## What's here

| File | What it does |
|---|---|
| `00personal_android_fixes.rpy` | Stops two crashes in a stock Ren'Py Android build: the `singleton` lock (no temp folder on Android) and the official app's custom Java music service, which the base game also calls when it starts from the desktop and when you change the music volume. |
| `00personal_pc_fixes.rpy` | For a Windows/PC build: makes the PC file checks (`renpy.file("../characters/monika.chr")` and the files next to the game) work on Ren'Py 8 again. Without it, a new game jumps straight to the Act 1 ending and Monika's room ends at once. Does nothing on Android. |
| `fix_poemgame.py` | Fixes a Python 3 error the decompiler left in `script-poemgame.rpy`. The game only starts today because the repo ships compiled bytecode; as soon as Ren'Py recompiles that file, it won't start. Run this first, whichever route you take. |
| `burmese_language.rpy` | Route A: adds "Burmese" to the desktop Settings app's language list, and switches every font the Japanese translation switches to your Myanmar font. |
| `burmese_fonts_in_place.rpy` | Route B: the same fonts, applied to the default language, for when the Burmese is written over the English. |

## Two ways to translate

- **Route A, translation files (`--tl`):** the Burmese goes into
  `game/tl/burmese/`, the English scripts stay untouched, and you pick
  Burmese in Settings. Needs the launcher's "Generate Translations" step.
- **Route B, in place (like your PC version):** the Burmese is written
  straight over the English in the `.rpy` scripts, and the game always shows
  it. No generating step, and you can see and edit the result directly in the
  scripts.

Use one or the other, not both.

## Route B: in place (like the PC version)

You need the Ren'Py 8.5 SDK on your PC.

1. Clone the repo:

   ```bash
   git clone https://github.com/HiroStuff/DDLC-Plus-Mobile
   ```

2. Fix the poem game:

   ```bash
   python3 plus-mobile/fix_poemgame.py path/to/DDLC-Plus-Mobile/game
   ```

3. Copy `00personal_android_fixes.rpy` and `burmese_fonts_in_place.rpy` into
   its `game/` folder, and put your font in `game/fonts/` as
   `Zawgyi-One.ttf` (or change `burmese_font` in that file).

4. Write your sheet over the English. Try it with `--dry-run` first:

   ```bash
   python3 tools/ddlc_xlsx.py apply script.xlsx --game path/to/DDLC-Plus-Mobile/game --dry-run
   python3 tools/ddlc_xlsx.py apply script.xlsx --game path/to/DDLC-Plus-Mobile/game
   ```

   This edits the scripts directly, the same as on PC. Commit or copy the
   `game/` folder first, so you can go back. Running it again with an updated
   sheet is safe: lines already translated no longer match their English and
   are left alone, and new rows get filled in. (To change a line that's
   already translated, edit it in the `.rpy` file, or restore the file and
   apply again.)

   To start a fresh sheet from the mobile scripts instead of your PC one:

   ```bash
   python3 tools/ddlc_xlsx.py extract path/to/DDLC-Plus-Mobile/game/script-ch0.rpy -o script-ch0.xlsx
   ```

5. Do steps 6 to 7 of route A (package name, build). Keep Settings on
   English: that's the language your Burmese is written into.

## Route A: translation files

You need the Ren'Py 8.5 SDK on your PC.

1. Clone the repo:

   ```bash
   git clone https://github.com/HiroStuff/DDLC-Plus-Mobile
   ```

2. Run `fix_poemgame.py` (see route B, step 2), then copy
   `00personal_android_fixes.rpy` and `burmese_language.rpy` from this
   folder into its `game/` folder.

3. Put your Myanmar font in `game/fonts/` as `Zawgyi-One.ttf`. If your font
   has a different name, change `burmese_font` at the top of
   `burmese_language.rpy`. Your sheet's text is Zawgyi-encoded, so it needs a
   Zawgyi font. A Unicode font such as Pyidaungsu will show it wrong.

4. In the Ren'Py launcher, open the project, click **Generate Translations**,
   type `burmese` as the language, and click **Generate Translations**. This
   creates `game/tl/burmese/` with one file per script, holding the English
   text ready to be replaced.

5. Fill it from your sheet with the tool in this repo:

   ```bash
   python3 tools/ddlc_xlsx.py apply script.xlsx --game path/to/DDLC-Plus-Mobile/game/tl/burmese --tl
   ```

   Each worksheet fills the file with the same name (sheet `script-ch0` →
   `tl/burmese/script-ch0.rpy`). Only the base game's script files need
   sheets. Run it again whenever your sheet changes; lines already translated
   are left alone because their English no longer matches.

6. Give your build its own package name, so it doesn't clash with the official
   app if that's also installed: in the launcher choose **Android** →
   **Configure**, and use something like `com.yourname.ddlc.burmese`. (That
   updates `android.json`, which still holds the official app's name.)

7. Build: **Android** → **Build Package**, then **Install** with the phone
   connected over USB, or copy the APK across.

8. In the game, open the desktop's **Settings** app and pick **Burmese**.

## Checking it

- Lines your sheet doesn't cover stay in English. `apply` lists rows whose
  English it couldn't find in the translation files. The mobile scripts are
  very close to the PC ones, so this should be rare.
- If Burmese letters are cut off at the top or bottom, the font needs more
  line spacing. Add `translate burmese style say_dialogue line_spacing 6` to
  `burmese_language.rpy` and raise the number until it looks right.
- Untested here: I couldn't build or run Android in this environment. If it
  crashes, the error is in `traceback.txt`, which the Android build shows on
  screen.

## Windows (PC) build

The same project builds for Windows. On PC the game uses real files again:
the `characters/` folder next to `game/`, and the files it drops beside the
game, like the original DDLC.

1. Do route A or B as above, but also copy `00personal_pc_fixes.rpy` into
   `game/`. (It can stay in for the Android build too.)
2. To just play on your PC, click **Launch Project** in the launcher.
3. To make a Windows copy you can move to another PC, click **Build
   Distributions**, tick **Windows**, and build. The result is a `.zip` in
   the folder next to your projects directory; unzip it and run
   `DDLC.exe`.

Notes:

- The repo's own code treats the Plus content as owned on PC, the way the
  Steam version works, so the side stories, gallery and other desktop apps
  open there instead of showing the purchase screen.
- The stream check uses `wmic`, which newer Windows 11 versions don't have.
  It fails quietly, so the game just doesn't notice streaming software.
