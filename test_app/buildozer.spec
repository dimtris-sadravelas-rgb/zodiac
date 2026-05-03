[app]

title = Zodiac App
package.name = zodiac
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg

version = 0.1

requirements = python3,kivy

orientation = portrait

# σημαντικά για android
android.api = 31
android.minapi = 21
android.sdk = 24
android.ndk = 23b

fullscreen = 0


[buildozer]

log_level = 2
warn_on_root = 1
