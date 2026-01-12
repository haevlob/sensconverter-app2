[app]

title = Sensitivity Converter

package.name = sensconverter
package.domain = org.devon  # изменил на уникальный

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

# Упрощённые requirements — надёжнее
requirements = python3,kivy==2.3.0

# Иконка (положи icon.png в корень проекта)
icon.filename = icon.png

# presplash.filename = presplash.png  # опционально

orientation = portrait
fullscreen = 1

# Убрал INTERNET — не нужен
# android.permissions = 

android.api = 34
android.minapi = 24
android.accept_sdk_license = True

p4a.bootstrap = sdl2
android.debug_artifact = apk

# Убрал старую версию NDK — Buildozer скачает свежую
# android.ndk = 

android.archs = arm64-v8a, armeabi-v7a

author = Devon
description = Конвертер чувствительности между Standoff 2, PUBG Mobile и CoD Mobile

[buildozer]

log_level = 2
warn_on_root = 1
