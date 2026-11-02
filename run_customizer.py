# -*- coding: utf-8 -*-
"""Sony α6700 Minimalist Customizer - Desktop App Launcher.

Entry point for both direct python execution and PyInstaller freeze.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Ensure vendor a6700win is importable
APP_DIR = PROJECT_ROOT / "apps" / "a6700_customizer"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from apps.a6700_customizer.app_gui import main

if __name__ == "__main__":
    main()
