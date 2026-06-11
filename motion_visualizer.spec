# -*- mode: python ; coding: utf-8 -*-

import os

# Укажи правильное имя файла (то, которое нашёл на шаге 1)
so_file = 'motion_core.cpython-313-x86_64-linux-gnu.so'  # или motion_core.cpython-313-x86_64-linux-gnu.so
so_path = os.path.join('src', 'motion_visualizer', 'cpp_bridge', so_file)

a = Analysis(
    ['src/motion_visualizer/main.py'],
    pathex=[],
    binaries=[],
    datas=[(so_path, 'cpp_bridge')],
    hiddenimports=[
        'PySide6.QtOpenGLWidgets',
        'sqlalchemy.sql.default_comparator',
        'OpenGL',
        'OpenGL.platform',
        'OpenGL.platform.glx',
        'OpenGL.platform.x11',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MotionVisualizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)