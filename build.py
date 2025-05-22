import PyInstaller.__main__
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'cvs-to-pgn-w-filters.py',
    '--name=CSVtoPGNConverter',
    '--onefile',
    '--windowed',
    '--icon=NONE',
    '--add-data=README.md;.',
    '--clean',
    '--noconfirm'
]) 