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
| `burmese_language.rpy` | Adds "Burmese" to the desktop Settings app's language list, and switches every font the Japanese translation switches to your Myanmar font. |

## Steps

You need the Ren'Py 8.5 SDK on your PC.

1. Clone the repo:

   ```bash
   git clone https://github.com/HiroStuff/DDLC-Plus-Mobile
   ```

2. Copy both `.rpy` files from this folder into its `game/` folder.

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
