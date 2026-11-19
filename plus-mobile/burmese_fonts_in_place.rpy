## Use this file instead of burmese_language.rpy when the translation is
## written straight over the English in the scripts (apply without --tl).
## The game then stays on its default language ("English" in Settings), so
## the Myanmar font is applied to that language here.
##
## Copy it into the game/ folder and put your Myanmar font in game/fonts/
## under the name below (or change the name). Don't use it together with
## burmese_language.rpy.

define burmese_font = "fonts/Zawgyi-One.ttf"

translate None python:
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

translate None style bios_text font burmese_font
translate None style confirm_prompt_text font burmese_font
translate None style console_text font burmese_font
translate None style edited font burmese_font
translate None style gallery_wallpaper_acquisition_text font burmese_font
translate None style gallery_wallpaper_description_text font burmese_font
translate None style jukebox_bold_text font burmese_font
translate None style mobile_captcha_text font burmese_font
translate None style monika_credits_text font burmese_font
translate None style monika_text font burmese_font
translate None style natsuki_text font burmese_font
translate None style navigation_button_text font burmese_font
translate None style quick_button_text font burmese_font
translate None style sayori_text font burmese_font
translate None style settings_bold_text font burmese_font
translate None style virtual_desktop_file_viewer_text font burmese_font
translate None style yuri_text font burmese_font
translate None style yuri_text_2 font burmese_font
translate None style yuri_text_3 font burmese_font
