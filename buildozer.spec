[app]

# Название приложения (отображается в лаунчере)
title = Sensitivity Converter

# Версия приложения
version = 1.0

# Пакетное имя (должно быть уникальным, например, для Google Play)
package.name = sensitivityconverter
package.domain = com.devon

# Директория с исходным кодом (текущая директория, где main.py)
source.dir = .

# Расширения файлов для включения в APK
source.include_exts = py,png,jpg,kv,atlas

# Требуемые зависимости (Python 3 и Kivy — достаточно для вашего кода)
requirements = python3,kivy

# Ориентация экрана (portrait — вертикальная, как в вашем коде с fullscreen)
orientation = portrait

# Полноэкранный режим (авто, как в коде)
fullscreen = auto

# Иконка приложения (если есть файл icon.png в корне, укажите путь)
# icon.filename = %(source.dir)s/icon.png

# Splash-экран (если есть, укажите путь)
# presplash.filename = %(source.dir)s/presplash.png

# Разрешения Android (вашему приложению не нужны специальные, но добавьте, если потребуется, например, для интернета)
# android.permissions = INTERNET

[buildozer]

# Уровень логирования (2 — детальный, полезно для отладки)
log_level = 2

# Предупреждать, если запускается от root
warn_on_root = 1
