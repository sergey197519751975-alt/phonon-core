[app]
title = PHONON-CORE
package.name = phononcore
package.domain = org.phonon
source.dir = .
source.include_exts = py,txt,png,jpg
version = 1.0
requirements = python==3.11.1,kivy==2.3.0
orientation = portrait
osx.kivy_version = 2.3.0
fullscreen = 1
android.python_version = 3.11
android.archs = armeabi-v7a, arm64-v8a
android.allow_backup = False
android.skip_assets_check = True

[buildozer]
log_level = 2
warn_on_root = 1
