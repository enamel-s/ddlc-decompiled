## Fixes for building the DDLC Plus mobile decompile with the stock Ren'Py
## Android tools, for personal use. Copy this file into the game/ folder.
##
## The file name starts with "00" so that its "python early" block runs
## before the one in definitions.rpy.

python early:
    import sys
    import types

    if renpy.mobile:
        # definitions.rpy imports singleton to stop two copies of the game
        # running at once. It puts a lock file in the temp folder, which
        # Android doesn't have, so the game would crash on start. A phone
        # can't run two copies anyway, so a stand-in module is used instead.
        _singleton = types.ModuleType("singleton")

        class SingleInstance(object):
            def __init__(self, *args, **kwargs):
                pass

        _singleton.SingleInstance = SingleInstance
        sys.modules["singleton"] = _singleton

init -999 python:
    if renpy.android:
        # The official app has a custom Java music service,
        # org.renpy.android.PlaybackService. Ren'Py's normal Android build
        # doesn't, so every call to it would crash, including the ones made
        # when the base game starts from the desktop and when the music
        # volume is changed. Asking for that class now returns an object
        # that quietly does nothing.
        import jnius

        class _NoPlaybackService(object):
            def __getattr__(self, name):
                return self._nothing

            def _nothing(self, *args, **kwargs):
                return 0

            def IsPlaying(self, *args, **kwargs):
                return False

        _real_autoclass = jnius.autoclass

        def _safe_autoclass(name, *args, **kwargs):
            try:
                return _real_autoclass(name, *args, **kwargs)
            except Exception:
                if name == "org.renpy.android.PlaybackService":
                    return _NoPlaybackService()
                raise

        jnius.autoclass = _safe_autoclass
