[app]
title = PHONON-CORE
package.name = phononcore
package.domain = org.phonon
source.dir = .
source.include_exts = py,txt,png,jpg
version = 1.0
requirements = python==3.12.0,kivy==2.3.0
orientation = portrait
osx.kivy_version = 2.3.0
fullscreen = 1
android.archs = armeabi-v7a, arm64-v8a
android.allow_backup = False

[buildozer]
log_level = 2
warn_on_root = 1

