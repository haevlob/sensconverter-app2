name: Build Kivy App

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install system dependencies
        run: |
          sudo apt update
          sudo apt install -y \
            python3-dev \
            build-essential \
            libgl1-mesa-dev \
            libgles2-mesa-dev \
            libgstreamer1.0-dev \
            gstreamer1.0-plugins-base \
            gstreamer1.0-plugins-good \
            gstreamer1.0-plugins-bad \
            gstreamer1.0-plugins-ugly \
            gstreamer1.0-libav \
            libsdl2-dev \
            libmtdev-dev \
            libxrandr-dev \
            libxinerama-dev \
            libxcursor-dev \
            libxi-dev

      - name: Upgrade pip
        run: python -m pip install --upgrade pip

      - name: Install Python dependencies
        run: |
          pip install kivy

      - name: Syntax check
        run: python -m py_compile main.py

      - name: Run basic import test
        run: python - << 'EOF'
import kivy
print('Kivy version:', kivy.__version__)
EOF
name: Build Kivy App

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install system dependencies
        run: |
          sudo apt update
          sudo apt install -y \
            python3-dev \
            build-essential \
            libgl1-mesa-dev \
            libgles2-mesa-dev \
            libgstreamer1.0-dev \
            gstreamer1.0-plugins-base \
            gstreamer1.0-plugins-good \
            gstreamer1.0-plugins-bad \
            gstreamer1.0-plugins-ugly \
            gstreamer1.0-libav \
            libsdl2-dev \
            libmtdev-dev \
            libxrandr-dev \
            libxinerama-dev \
            libxcursor-dev \
            libxi-dev

      - name: Upgrade pip
        run: python -m pip install --upgrade pip

      - name: Install Python dependencies
        run: |
          pip install kivy

      - name: Syntax check
        run: python -m py_compile main.py

      - name: Run basic import test
        run: python - << 'EOF'
import kivy
print('Kivy version:', kivy.__version__)
EOF
