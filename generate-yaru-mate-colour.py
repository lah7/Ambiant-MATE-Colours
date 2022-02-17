#!/usr/bin/python3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2021 Luke Horwell <code@horwell.me>
#

from modules.common import validate_colour_hex
from modules.common import check_for_tool
from modules.common import get_output
from modules.hexrgb import get_hex_variant
from modules.hexrgb import is_dark_colour
from modules.graphics import colourize_raster
from modules.postprocessing import optimise_icon_size
from modules.strings import replace_string

import argparse
import glob
import tempfile
import os
import shutil
import subprocess


def _run(action, command):
    print(action)
    subprocess.check_output(command.split(" "))


# ------------------------------------------------
# Check tools are present
# ------------------------------------------------
check_for_tool("git")
check_for_tool("meson")
check_for_tool("sassc")
check_for_tool("inkscape")
check_for_tool("optipng")
# Needs "libglib2.0-bin"
# Needs "libgtk-3-dev"


# ------------------------------------------------
# Variables and parameter parsing
# ------------------------------------------------
parser = argparse.ArgumentParser()
parser._optionals.title = "Required Arguments"

# Required
parser.add_argument("--hex", metavar="CODE", help="Colour value to use, e.g. '#2DACD4'", action="store")
parser.add_argument("--name", metavar="NAME", help="Human readable suffix to identify variant, e.g. 'Aqua'.", action="store")
parser.add_argument("--src-dir", metavar="PATH", help="Path to Yaru-MATE source code", action="store")
parser.add_argument("--usr-dir", metavar="PATH", help="Path to usr/ output directory", action="store")
args = parser.parse_args()

if None in [args.hex, args.name, args.src_dir, args.usr_dir]:
    print("One (or more) parameters are invalid or missing. See --help for usage.")
    exit(1)

if len(args.hex) == 6:
    args.hex = "#" + args.hex

HEX_VALUE = args.hex
THEME_NAME = args.name
SRC_DIR = os.path.realpath(args.src_dir)
TEMP_DIR = tempfile.mktemp()
PREFIX_DIR = os.path.realpath(args.usr_dir)

if not validate_colour_hex(args.hex):
    print("Invalid hex value!")
    print("Values should be in long format: #FFFFFF")
    print("(If the input starts with '#', make sure to wrap with quotes)")
    exit(1)

if len(THEME_NAME) == 0:
    print("Invalid theme name!")
    exit(1)

if not os.path.exists(SRC_DIR):
    print("This does not appear to be the Yaru-MATE repository:")
    print(SRC_DIR)
    exit(1)


# ------------------------------------------------
# Patch source
# ------------------------------------------------
print("\nGenerating Yaru-MATE-{0} ({1})...\n".format(THEME_NAME, HEX_VALUE))
print("Yaru-MATE Source:     ", SRC_DIR)
print("Temporary build path: ", TEMP_DIR)
print("Destination:          ", PREFIX_DIR)
print("")

print("Copying source files...")
shutil.copytree(SRC_DIR, TEMP_DIR, symlinks=True, ignore_dangling_symlinks=True)

print("Patching colours...")

# Patch name
os.chdir(TEMP_DIR)
replace_string(["meson.build"], "Yaru-MATE", "Yaru-MATE-" + THEME_NAME)

# Patch colours
replace_string(["*.svg", "*.scss", "*.css"], "#87A556", HEX_VALUE)
replace_string(["*.svg", "*.scss", "*.css"], "#87a556", HEX_VALUE)

# Patch theme colours
replace_string(["*.svg", "*.scss", "*.css"], "#5c853d", get_hex_variant(HEX_VALUE, -8))
replace_string(["*.svg", "*.scss", "*.css"], "#79944d", get_hex_variant(HEX_VALUE, -4))
replace_string(["*.svg", "*.scss", "*.css"], "#7DAF56", get_hex_variant(HEX_VALUE, 2))
replace_string(["*.svg", "*.scss", "*.css"], "#9bb571", get_hex_variant(HEX_VALUE, 2.2))
replace_string(["*.svg", "*.scss", "*.css"], "#83B35C", get_hex_variant(HEX_VALUE, 2))
replace_string(["*.svg", "*.scss", "*.css"], "#8aa858", get_hex_variant(HEX_VALUE, 2))
replace_string(["*.svg", "*.scss", "*.css"], "#89B763", get_hex_variant(HEX_VALUE, 2.2))
replace_string(["*.svg", "*.scss", "*.css"], "#8FBB69", get_hex_variant(HEX_VALUE, 2.4))
replace_string(["*.svg", "*.scss", "*.css"], "#93af66", get_hex_variant(HEX_VALUE, 2.5))
replace_string(["*.svg", "*.scss", "*.css"], "#95BF70", get_hex_variant(HEX_VALUE, 2.6))
replace_string(["*.svg", "*.scss", "*.css"], "#A1C77D", get_hex_variant(HEX_VALUE, 2.8))
replace_string(["*.svg", "*.scss", "*.css"], "#A7CB83", get_hex_variant(HEX_VALUE, 3))
replace_string(["*.svg", "*.scss", "*.css"], "#ADD08A", get_hex_variant(HEX_VALUE, 3.2))

# Patch icon colours
# -- user-desktop.svg
replace_string("*.svg", "#93b258", get_hex_variant(HEX_VALUE, 2.5))
replace_string("*.svg", "#5d8638", get_hex_variant(HEX_VALUE, -8))
replace_string("*.svg", "#eaffcf", "#ffffff")

# -- folders.svg
replace_string("*.svg", "#b4d959", get_hex_variant(HEX_VALUE, 12))
replace_string("*.svg", "#45602a", get_hex_variant(HEX_VALUE, -12))

# Patch cursor colours
replace_string("*.svg", "#19b6ee", HEX_VALUE)


# ------------------------------------------------
# Pre-build
# ------------------------------------------------
print("Rendering cursors...")
os.chdir(TEMP_DIR + "/icons/src/cursors/")
os.system("./x11-make.sh")

print("Rendering icons...\n--------------------------------")
os.chdir(TEMP_DIR + "/icons/src/fullcolor/")
changed_icons = [
    "preferences-desktop-wallpaper",
    "emblem-symbolic-link",
    "emblem-synchronizing",
    "document-export",
    "document-open",
    "folders",
    "user-desktop"
]
for icon in changed_icons:
    os.system("./render-bitmaps.py " + icon)
print("\n--------------------------------\n")

# ------------------------------------------------
# Build
# ------------------------------------------------
os.chdir(TEMP_DIR)
_run("Preparing meson build...", "meson build --prefix=" + PREFIX_DIR)

# Patch strings
os.system("sed -i 's/Yaru-MATE/Yaru-MATE-{0}/g' meson.build".format(THEME_NAME))
os.system("sed -i 's/Ambiant-MATE/Yaru-MATE-dark,Ambiant-MATE/g' icons/meson.build")
os.system("sed -i 's/Radiant-MATE/Yaru-MATE-light,Radiant-MATE/g' icons/meson.build")

os.chdir("build")
_run("Configuring meson... (build type)", "meson configure -Dbuildtype=release")
_run("Configuring meson... (set prefix)", "meson configure -Dprefix=" + PREFIX_DIR)
_run("Configuring meson... (disable gnome-shell)", "meson configure -Dgnome-shell=false")
_run("Configuring meson... (disable gnome-shell-gresource)", "meson configure -Dgnome-shell-gresource=false")
_run("Configuring meson... (disable ubuntu-unity)", "meson configure -Dubuntu-unity=false")
_run("Configuring meson... (disable sessions)", "meson configure -Dsessions=false")
_run("Configuring meson... (disable sounds)", "meson configure -Dsounds=false")

# Put it in the oven!
os.chdir("..")
_run("Building...", "ninja -C build install")

print("Recolouring GTK2 assets...")
os.chdir(PREFIX_DIR + "/share/themes/")
for theme in glob.glob("*"):
    for asset in [
        "checkbox-checked.png",
        "checkbox-checked-active.png",
        "checkbox-mixed.png",
        "checkbox-mixed-active.png",
        "combo-entry-ltr-entry-active.png",
        "combo-entry-rtl-entry-active.png",
        "entry-active.png",
        "focus.png",
        "menubar-item-active.png",
        "menu-checkbox-checked.png",
        "menu-checkbox-mixed.png",
        "menu-radio-checked.png",
        "menu-radio-mixed.png",
        "notebook-combo-entry-ltr-entry-active.png",
        "notebook-combo-entry-rtl-entry-active.png",
        "notebook-entry-active.png",
        "progressbar-horz.png",
        "progressbar-vert.png",
        "radio-checked.png",
        "radio-checked-active.png",
        "radio-mixed.png",
        "radio-mixed-active.png",
        "scale-horz-trough-active.png",
        "scale-slider-active.png",
        "scale-vert-trough-active.png",
        "scrollbar-horz-slider-active.png",
        "scrollbar-vert-slider-active.png",
        "scrollbar-vert-slider-active-rtl.png"
    ]:
        asset_path = os.path.join(theme, "gtk-2.0", "assets", asset)
        colourize_raster(HEX_VALUE, asset_path)


# ------------------------------------------------
# Finishing up
# ------------------------------------------------
print("Cleaning up temporary files...")
shutil.rmtree(TEMP_DIR)

# Reduce disk space by removing duplicates of unchanged icons
if os.path.exists("/usr/share/icons/Yaru-MATE-light/"):
    new_icons_prefix = os.path.join(PREFIX_DIR, "share/icons/Yaru-MATE-" + THEME_NAME)
    optimise_icon_size(SRC_DIR + "/icons/Suru/", new_icons_prefix)
    optimise_icon_size(SRC_DIR + "/icons/Suru/", new_icons_prefix + "-dark")
    optimise_icon_size(SRC_DIR + "/icons/Suru/", new_icons_prefix + "-light")
else:
    print("\nWARNING: Yaru-MATE is not installed on system! Skipping icon disk space optimisation.\n")

print("\nSuccessfully generated Yaru-MATE-{0} ({1})\nSaved to: {2}\n".format(THEME_NAME, HEX_VALUE, PREFIX_DIR))
