## Adds Burmese as a language. Copy this file into the game/ folder, and put
## your Myanmar font in game/fonts/ under the name below (or change the name).
##
## This follows the way the game sets up its Japanese translation: the same
## gui fonts and styles are switched to the Burmese font when Burmese is
## selected in the desktop's Settings app.

define burmese_font = "fonts/Zawgyi-One.ttf"

init 10 python:
    # Add Burmese to the language list in the desktop Settings app. The name
    # is written in English because the settings font has no Myanmar letters.
    if "burmese" not in settings_available_languages:
        settings_available_languages.append("burmese")
        settings_localized_languages.append("Burmese")

translate burmese python:
    gui.text_font = burmese_font
    gui.name_text_font = burmese_font
    gui.riffic_font = burmese_font
    gui.halogen_font = burmese_font
    gui.virtual_desktop_text_font = burmese_font
    gui.virtual_desktop_bold_text_font = burmese_font
    gui.virtual_desktop_black_text_font = burmese_font
    gui.virtual_desktop_start_text_font = burmese_font
    gui.choice_button_text_font = burmese_font
    gui.interface_text_font = burmese_font

translate burmese style bios_text font burmese_font
translate burmese style confirm_prompt_text font burmese_font
translate burmese style console_text font burmese_font
translate burmese style edited font burmese_font
translate burmese style gallery_wallpaper_acquisition_text font burmese_font
translate burmese style gallery_wallpaper_description_text font burmese_font
translate burmese style jukebox_bold_text font burmese_font
translate burmese style mobile_captcha_text font burmese_font
translate burmese style monika_credits_text font burmese_font
translate burmese style monika_text font burmese_font
translate burmese style natsuki_text font burmese_font
translate burmese style navigation_button_text font burmese_font
translate burmese style quick_button_text font burmese_font
translate burmese style sayori_text font burmese_font
translate burmese style settings_bold_text font burmese_font
translate burmese style virtual_desktop_file_viewer_text font burmese_font
translate burmese style yuri_text font burmese_font
translate burmese style yuri_text_2 font burmese_font
translate burmese style yuri_text_3 font burmese_font
