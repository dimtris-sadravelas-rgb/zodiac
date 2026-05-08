[app]

title = Birth Zodiac Finder
package.name = birthzodiacfinder
package.domain = gr.sadravelas
version = 0.2

source.dir = .
source.include_exts = py,png,jpg,json
android.permissions = INTERNET
requirements = python3,kivy

orientation = portrait

android.archs = arm64-v8a, armeabi-v7a
android.api = 31
android.minapi = 23
android.ndk = 25b
android.accept_sdk_license = True

fullscreen = 0


[buildozer]

log_level = 2
warn_on_root = 1
