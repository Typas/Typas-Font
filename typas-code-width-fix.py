# modified from https://github.com/lxgw/LxgwWenkaiTC/blob/main/sources/fix_mono.py
from fontTools.ttLib import TTFont
import os, sys

directory = sys.argv[1]

for file in os.listdir(directory):
    if "ttf" not in file:
        continue

    font_path = os.path.join(directory, file)
    font = TTFont(font_path)
    font["head"].unitsPerEm = 1950
    font.save(font_path, reorderTables=False)

