# modified from https://github.com/lxgw/LxgwWenkaiTC/blob/main/sources/fix_mono.py
from fontTools.ttLib import TTFont
import os, sys

directory = sys.argv[1]

JULIAMONO_MAJOR = 0
JULIAMONO_MINOR = 50
FIRACODE_MAJOR = 6
FIRACODE_MINOR = 200
MAJOR = JULIAMONO_MAJOR + FIRACODE_MAJOR
MINOR = JULIAMONO_MINOR + FIRACODE_MINOR
VERSION = "{}.{:03}".format(MAJOR, MINOR)

def is_italic(name):
    return "Italic" in name

def fix_family(names):
    long_name = names.getDebugName(4)
    family_base = "Typas Code"
    if "Light" in long_name:
        return family_base + " Light"
    elif "Medium" in long_name:
        return family_base + " Medium"
    elif "SemiBold" in long_name:
        return family_base + " SemiBold"
    else:
        return family_base

def fix_subfamily(names):
    long_name = names.getDebugName(4)
    if "Light" or "Medium" or "SemiBold" in long_name:
        if "Italic" in long_name:
            return "Italic"
        else:
            return "Regular"
    elif "Bold" in long_name:
        if "Italic" in long_name:
            return "Bold Italic"
        else:
            return "Bold"
    else:
        if "Italic" in long_name:
            return "Italic"
        else:
            return "Regular"

def weight(names):
    long_name = names.getDebugName(4)
    if "Light" in long_name:
        return "Light"
    elif "Medium" in long_name:
        return "Medium"
    elif "SemiBold" in long_name:
        return "SemiBold"
    elif "Bold" in long_name:
        return "Bold"
    elif "Italic" in long_name:
        return ""
    else:
        return "Regular"

def fix_unique_identifier(names):
    unique_id = VERSION + ";UKWN;"
    unique_id += fix_postscript(names)
    return unique_id

def fix_full_font_name(names):
    # base name
    full_font_name = "Typas Code"
    # weight
    w = weight(names)
    if w != "":
        full_font_name += " " + w
    # italic
    if "Italic" in names.getDebugName(4):
        full_font_name += " Italic"
    return full_font_name

def fix_version(_):
    return "Version " + VERSION

def fix_postscript(names):
    postscript = "TypasCode-"
    postscript += weight(names)
    if "Italic" in names.getDebugName(4):
        postscript += "Italic"
    return postscript

for file in os.listdir(directory):
    if "ttf" not in file:
        continue

    font_path = os.path.join(directory, file)
    font = TTFont(font_path)
    font["OS/2"].achVendID = "UKWN" # set to unknown vendor
    font["head"].unitsPerEm = 1950
    font["name"].removeNames(18)
    names = font["name"]
    for name in font["name"].names:
        match name.nameID:
            case 1:
                font["name"].setName(fix_family(names), 1, name.platformID, name.platEncID, name.langID)
            case 2:
                font["name"].setName(fix_subfamily(names), 2, name.platformID, name.platEncID, name.langID)
            case 3:
                font["name"].setName(fix_unique_identifier(names), 3, name.platformID, name.platEncID, name.langID)
            case 4:
                font["name"].setName(fix_full_font_name(names), 4, name.platformID, name.platEncID, name.langID)
            case 5:
                font["name"].setName(fix_version(names), 5, name.platformID, name.platEncID, name.langID)
            case 6:
                font["name"].setName(fix_postscript(names), 6, name.platformID, name.platEncID, name.langID)
    font.save(font_path, reorderTables=False)
    print(file, "has been processed")
