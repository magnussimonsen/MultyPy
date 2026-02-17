# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for MultiPy
This file configures how the application is built into an executable.
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os
import sys

# Define base directory
block_cipher = None

# Collect Textual and Rich data files (CRITICAL for TUI apps)
datas = []
datas += collect_data_files('textual')
datas += collect_data_files('rich')

# Manually add rich._unicode_data if needed
try:
    import rich._unicode_data
    unicode_data_dir = os.path.dirname(rich._unicode_data.__file__)
    datas.append((unicode_data_dir, 'rich/_unicode_data'))
except ImportError:
    pass

# Collect hidden imports for our app structure
# This ensures PyInstaller finds all our modules even if dynamic imports are used
hidden_imports = [
    'textual',
    'rich',
    # App modules
    'multipy',
    'multipy.app',
    'multipy.models',
    'multipy.services',
    'multipy.services.math_generator',
    'multipy.services.metrics',
    'multipy.views',
    'multipy.views.menu_view',
    'multipy.views.practice_view',
    'multipy.views.summary_view',
    'multipy.views.about_view',
]

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MultiPy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
