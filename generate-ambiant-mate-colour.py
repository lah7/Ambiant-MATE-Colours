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
# Copyright (C) 2019-2022 Luke Horwell <code@horwell.me>
#
"""
Ambiant-MATE and Radiant-MATE family of themes don't have a build system,
so this script is a search & replace operation to extract the old colour
and switch it with new ones.

This script handles the parameters to produce a new GTK theme, icons, as well
as the wallpapers. Optional tweaks may include some patches on top of that.
"""
import argparse
import os
import shutil

from modules.common import validate_colour_hex
from modules.graphics import export_svg
from modules.graphics import colourize_raster
from modules.hexrgb import get_hex_variant
from modules.hexrgb import get_rgb_variant_of_hex
from modules.hexrgb import hex_to_rgb
from modules.hexrgb import hex_to_rgba
from modules.hexrgb import hex_to_rgb_list
from modules.hexrgb import get_hex_variant
from modules.postprocessing import optimise_icon_size
from modules.strings import replace_string


SUPPORTED_THEMES = [
    "Ambiant-MATE",
    "Radiant-MATE",
    "Ambiant-MATE-Dark"
]

THEME_TO_ICONS = {
    "Ambiant-MATE": "Ambiant-MATE",
    "Ambiant-MATE-Dark": "Ambiant-MATE",
    "Radiant-MATE": "Radiant-MATE"
}


# ------------------------------------------------
# Variables and parameter parsing
# ------------------------------------------------
class Properties(object):
    def __init__(self):
        # Source
        self.base_theme = ""
        self.base_icon_theme = ""
        self.base_wallpapers = ""
        self.src_path = None

        if os.path.exists(os.path.dirname(__file__) + "/templates"):
            self.templates_dir = os.path.realpath(os.path.dirname(__file__)) + "/templates"
        elif os.path.exists("/usr/share/ubuntu-mate-colours/"):
            self.templates_dir = "/usr/share/ubuntu-mate-colours/templates"
        else:
            print("'templates' directory missing!")
            exit(1)

        # Names
        self.new_name = ""
        self.new_hex_value = ""
        self.new_theme_name = ""
        self.new_icon_name = ""
        self.new_wallpaper_dirname = ""

        # Destination paths
        self.target_dir_icons = os.path.expanduser("~/.icons")
        self.target_dir_theme = os.path.expanduser("~/.themes")
        self.target_dir_wallpapers = os.path.expanduser("~/.local/share/backgrounds")
        self.target_share_path = os.path.expanduser("~/.local/share")
        self.target_wallpapers_xml = os.path.expanduser("~/.local/share/mate-background-properties")

        # Build parameters
        self.always_overwrite = False
        self.ignore_existing = False
        self.build_theme = True
        self.build_icons = True
        self.build_wallpapers = True
        self.packaging = False
        self.tweaks = []


def parse_arguments():
    """
    Processes the parameters (arguments) for command line usage.
    """
    parser = argparse.ArgumentParser()
    parser._optionals.title = "Avaliable Arguments"

    # Required
    parser.add_argument("--theme", metavar="NAME", help="Required. Ubuntu MATE theme to use, e.g. 'Ambiant-MATE'", action="store")
    parser.add_argument("--hex", metavar="CODE", help="Required. Colour value to use, e.g. '#5489CF'", action="store")
    parser.add_argument("--name", metavar="NAME", help="Required. Human readable suffix to identify variant, e.g. 'Blue'.", action="store")
    parser.add_argument("--src-dir", metavar="PATH", help="Required. Path to ubuntu-mate-artwork repository", action="store")

    # Optional
    parser.add_argument("--install-icon-dir", metavar="PATH", help="Path to install coloured icons", action="store")
    parser.add_argument("--install-theme-dir", metavar="PATH",help="Path to install coloured theme", action="store")
    parser.add_argument("--install-wallpapers-dir", metavar="PATH", help="Path to install coloured wallpapers", action="store")
    parser.add_argument("--install-share-dir", metavar="PATH", help="Path to install /usr/share path for additional files", action="store")
    parser.add_argument("-y", "--overwrite", help="Suppress confirmation prompt if target exists", action="store_true")
    parser.add_argument("-i", "--ignore-existing", help="Ignore target folders that already exist", action="store_true")
    parser.add_argument("--list-tweaks", help="List available modifications", action="store_true")
    parser.add_argument("--tweaks", help="Apply additional modifications, comma separated", action="store")

    # Special consideration for packaging use only
    parser.add_argument( "--packaging", help=argparse.SUPPRESS, action="store_true")

    args = parser.parse_args()

    if args.list_tweaks:
        print("Available Tweaks")
        print("-----------------------  -----------------------------------------------------")
        for tweak in tweaks.tweaks.keys():
            description = tweaks.tweaks[tweak][1]
            print("                         " + description, end="")
            print("\r" + tweak)
        exit(0)

    if None in [args.theme, args.hex, args.name, args.src_dir]:
        print("Missing one of the required arguments: --theme, --hex, --name, --src-dir")
        print("See --help for details.")
        exit(1)

    if args.theme:
        prop.base_theme = args.theme

        if prop.base_theme not in SUPPORTED_THEMES:
            print("Unsupported theme: " + prop.base_theme)
            exit(1)

        prop.base_icon_theme = THEME_TO_ICONS[prop.base_theme]

        if prop.base_theme.startswith("Yaru"):
            print("Yaru-MATE is not supported by this script.")
            print("See README for details on generating Yaru-MATE variants.")
            exit(1)

    if args.hex:
        if len(args.hex) == 6:
            args.hex = "#" + args.hex

        if not validate_colour_hex(args.hex):
            print("Invalid hex value: " + args.hex)
            print("Values should be in long format: #FFFFFF")
            print("(If the input starts with '#', make sure to wrap with quotes)")
            exit(1)

        prop.new_hex_value = args.hex

    if args.name:
        prop.new_name = args.name
        prop.new_theme_name = prop.base_theme + "-" + args.name
        prop.new_icon_name = prop.base_icon_theme + "-" + prop.new_name
        prop.new_wallpaper_dirname = "ubuntu-mate-colours-" + prop.new_name.lower()

    if args.src_dir:
        prop.src_path = os.path.realpath(args.src_dir)

        if not os.path.exists(args.src_dir):
            print("Could not find: " + args.src_dir)
            exit(1)

        if not os.path.exists(os.path.join(prop.src_path, "usr/share/themes/", prop.base_theme)):
            print("Could not locate theme: " + prop.base_theme)
            exit(1)

    if args.install_icon_dir:
        prop.target_dir_icons = args.install_icon_dir

    if args.install_theme_dir:
        prop.target_dir_theme = args.install_theme_dir

    if args.install_wallpapers_dir:
        prop.target_dir_wallpapers = args.install_wallpapers_dir

    if args.install_share_dir:
        prop.target_share_path = os.path.realpath(args.install_share_dir)
        prop.target_wallpapers_xml = os.path.join(args.install_share_dir, "mate-background-properties")

    if args.packaging:
        prop.packaging = True

    if args.overwrite:
        prop.always_overwrite = True

    if args.ignore_existing:
        prop.ignore_existing = True

    if args.tweaks:
        prop.tweaks = args.tweaks.split(",")

        # Validate for any invalid tweaks
        for tweak in prop.tweaks:
            try:
                tweaks.tweaks[tweak]
            except KeyError:
                print("Invalid tweak name: " + tweak)
                print("Use --list-tweaks to view available options.")
                exit(1)


# ------------------------------------------------
# Prepare a copy of the theme for patching
# ------------------------------------------------
def prep_targets():
    """
    Create copy of repository and perform the modifications.
    """
    def _copy_tree(item, src, dst):
        print("Copying {0} files...".format(item))

        if os.path.exists(dst):
            if prop.ignore_existing and item == "theme":
                prop.build_theme = False
                print("Skipped as target theme exists.\n")
                return

            if prop.ignore_existing and item == "icons":
                prop.build_icons = False
                print("Skipped as target icon exists.\n")
                return

            if not prop.always_overwrite and not prop.ignore_existing:
                print("\nDirectory exists: " + dst)
                if input("Type 'y' to confirm removal: ") != "y":
                    exit(1)

            shutil.rmtree(dst)

        shutil.copytree(src, dst, symlinks=True)
        print("Copied.\n")

    prop.target_dir_theme = os.path.realpath(os.path.join(prop.target_dir_theme, prop.new_theme_name))
    prop.target_dir_icons = os.path.realpath(os.path.join(prop.target_dir_icons, prop.new_icon_name))
    prop.target_dir_wallpapers = os.path.realpath(os.path.join(prop.target_dir_wallpapers, prop.new_wallpaper_dirname))
    prop.target_wallpapers_xml = os.path.realpath(os.path.join(prop.target_wallpapers_xml, prop.new_wallpaper_dirname + ".xml"))
    prop.target_plank_theme = os.path.join(prop.target_share_path, "plank", "themes", "Ubuntu-MATE-" + prop.new_name, "dock.theme")

    _copy_tree("theme", os.path.join(prop.src_path, "usr/share/themes/", prop.base_theme), prop.target_dir_theme)
    _copy_tree("icon", os.path.join(prop.src_path, "usr/share/icons/", prop.base_icon_theme), prop.target_dir_icons)

    # Check wallpaper directory/XML file as these process the source files directly.
    if os.path.exists(prop.target_dir_wallpapers):
        if prop.ignore_existing:
            print("Skipping wallpaper generation as target exists.\n")
            prop.build_wallpapers = False

        elif prop.always_overwrite:
            print("\nDirectory exists: " + prop.target_dir_wallpapers)
            shutil.rmtree(prop.target_dir_wallpapers)
            if os.path.exists(prop.target_wallpapers_xml):
                os.remove(prop.target_wallpapers_xml)

    if not os.path.exists(prop.target_dir_wallpapers):
        print("Created wallpaper directory.\n")
        os.makedirs(prop.target_dir_wallpapers)

    if not os.path.exists(os.path.dirname(prop.target_wallpapers_xml)):
        print("Created mate-background-properties directory.\n")
        os.makedirs(os.path.dirname(prop.target_wallpapers_xml))

    if not os.path.exists(os.path.dirname(prop.target_plank_theme)):
        print("Created plank theme directory.\n")
        os.makedirs(os.path.dirname(prop.target_plank_theme))

    print("Source files copied.\n")


# ------------------------------------------------
# Perform the theme and icon patches!
# ------------------------------------------------
def patch_theme():
    """
    Search through the theme and replace green with new values.
    """
    os.chdir(os.path.realpath(prop.target_dir_theme))

    if not prop.build_theme:
        return

    print("Patching theme...")

    # --> Metadata
    replace_string("index.theme", "Name=" + prop.base_theme, "Name=" + prop.new_theme_name)
    replace_string("index.theme", "GtkTheme=" + prop.base_theme, "GtkTheme=" + prop.new_theme_name)
    replace_string("index.theme", "MetacityTheme=" + prop.base_theme, "MetacityTheme=" + prop.new_theme_name)
    replace_string("index.theme", "IconTheme=" + prop.base_icon_theme, "IconTheme=" + prop.new_icon_name)
    replace_string("index.theme", "Comment=", "Comment=" + prop.new_name + " ")
    replace_string("metacity-theme-1.xml", "<name>{0}</name>".format(prop.base_theme), "<name>{0}</name>".format(prop.new_theme_name))

    # --> Base colour
    replace_string(["*.ini", "gtkrc"], "#87A752", prop.new_hex_value) # <= 19.10
    replace_string(["*.ini", "gtkrc"], "#87A556", prop.new_hex_value) # >= 20.04 (Official)
    replace_string(["*.ini", "gtkrc", "*.css"], "#A7BB85", get_hex_variant(prop.new_hex_value, -21))

    replace_string("*.css", "#87A752", prop.new_hex_value) # <= 19.10
    replace_string("*.css", "#87A556", prop.new_hex_value) # >= 20.04 (Official)
    replace_string("*.css", hex_to_rgb("#87A752"), hex_to_rgb(prop.new_hex_value)) # <= 19.10
    replace_string("*.css", hex_to_rgb("#87A556"), hex_to_rgb(prop.new_hex_value)) # >= 20.04 (Official)
    replace_string("*.css", hex_to_rgba("#87A752"), hex_to_rgba(prop.new_hex_value)) # <= 19.10
    replace_string("*.css", hex_to_rgba("#87A556"), hex_to_rgba(prop.new_hex_value)) # >= 20.04 (Official)
    replace_string("*.css", "#84b436", get_hex_variant(prop.new_hex_value, 5))
    replace_string("*.css", hex_to_rgba("#84b436"), hex_to_rgba(prop.new_hex_value))

    # --> Ambiant-MATE Assets
    replace_string("*.svg", "#87A752", prop.new_hex_value) # <= 19.10
    replace_string("*.svg", "#87A556", prop.new_hex_value) # >= 20.04 (Official)
    replace_string("*.svg", "#355404", get_hex_variant(prop.new_hex_value, -32))
    replace_string("*.svg", "#5a782c", get_hex_variant(prop.new_hex_value, -17))
    replace_string("*.svg", "#64941c", get_hex_variant(prop.new_hex_value, -14))
    replace_string("*.svg", "#79a934", get_hex_variant(prop.new_hex_value, -6))
    replace_string("*.svg", "#87a556", get_hex_variant(prop.new_hex_value, 1))
    replace_string("*.svg", "#96b565", get_hex_variant(prop.new_hex_value, 6))

    # --> Ambiant-MATE: Close button (normal)
    replace_string(["*.svg", "gtk-widgets.css"], "#de4c19", get_hex_variant(prop.new_hex_value, 8))
    replace_string(["*.svg", "gtk-widgets.css"], "#e55e30", get_hex_variant(prop.new_hex_value, 12))
    replace_string(["*.svg", "gtk-widgets.css"], "#f58d6e", get_hex_variant(prop.new_hex_value, 16))

    # --> Ambiant-MATE: Close button (prelight)
    replace_string(["*.svg", "gtk-widgets.css"], "#e24f1b", get_hex_variant(prop.new_hex_value, 20))
    replace_string(["*.svg", "gtk-widgets.css"], "#f17750", get_hex_variant(prop.new_hex_value, 24))
    replace_string(["*.svg", "gtk-widgets.css"], "#fba992", get_hex_variant(prop.new_hex_value, 28))

    # --> Ambiant-MATE: Close button (pressed)
    replace_string(["*.svg", "gtk-widgets.css"], "#ec6e44", get_hex_variant(prop.new_hex_value, -4))
    replace_string(["*.svg", "gtk-widgets.css"], "#e76b41", get_hex_variant(prop.new_hex_value, 0))

    # --> Radiant-MATE: Close button (normal)
    replace_string(["*.svg", "gtk-widgets.css"], "#e77041", get_hex_variant(prop.new_hex_value, 8))
    replace_string(["*.svg", "gtk-widgets.css"], "#f17d4e", get_hex_variant(prop.new_hex_value, 12))
    replace_string(["*.svg", "gtk-widgets.css"], "#f9b39c", get_hex_variant(prop.new_hex_value, 16))

    # --> Radiant-MATE: Close button (prelight)
    replace_string(["*.svg", "gtk-widgets.css"], "#e67144", get_hex_variant(prop.new_hex_value, 20))
    replace_string(["*.svg", "gtk-widgets.css"], "#ed8b67", get_hex_variant(prop.new_hex_value, 24))
    replace_string(["*.svg", "gtk-widgets.css"], "#f9cbbd", get_hex_variant(prop.new_hex_value, 28))

    # --> Radiant-MATE: Close button (pressed)
    replace_string(["*.svg", "gtk-widgets.css"], "#f08054", get_hex_variant(prop.new_hex_value, -4))
    replace_string(["*.svg", "gtk-widgets.css"], "#f07c4e", get_hex_variant(prop.new_hex_value, 0))

    print("Theme patched.\n")

    # Export new PNGs for SVGs in the theme (button border, close, etc)
    print("Generating theme assets...")
    os.chdir(os.path.realpath(prop.target_dir_theme))

    # GTK3 assets
    for asset in [
        "check-mixed",
        "check-mixed-alt",
        "check-mixed-hover",
        "check-mixed-hover-alt",
        "check-selected-alt",
        "check-selected-hover-alt",
        "check-selected-hover",
        "check-selected",
        "radio-mixed-alt",
        "radio-mixed-hover",
        "radio-mixed-hover-alt",
        "radio-mixed",
        "radio-selected-alt",
        "radio-selected-hover-alt",
        "radio-selected-hover",
        "radio-selected"]:
            export_svg(prop, "gtk-3.0/assets/" + asset + ".svg", "gtk-3.0/assets/" + asset + ".png")
            export_svg(prop, "gtk-3.0/assets/" + asset + ".svg", "gtk-3.0/assets/" + asset + "@2.png")

    # For some reason, Radiant-MATE has a different filename for "close_focused_normal"
    if prop.base_icon_theme == "Radiant-MATE":
        shutil.copy("unity/close_focused.svg", "unity/close_focused_normal.svg")

    # Metacity assets
    for asset in [
        "close_focused_normal",
        "close_focused_prelight",
        "close_focused_pressed",
        "close"]:
            export_svg(prop, "unity/" + asset + ".svg", "metacity-1/" + asset + ".png")

    # Remove unity assets as unused
    unity_dir = os.path.join(prop.target_dir_theme, "unity")
    if os.path.exists(unity_dir):
        shutil.rmtree(unity_dir)

    # Generate colourised variants of PNGs (as SVG may not be available)
    for asset in [
        # Ambiant/Radiant-MATE
        "button-active-focused",
        "button-active-focused-hover",
        "button-active-hover",
        "button-default-focused",
        "button-default-focused-hover",
        "button-focused",
        "button-focused-hover",
        "button-toolbar-active-focused",
        "button-toolbar-focused",
        "check-selected",
        "combobox-button-focused",
        "combobox-button-pressed-focused",
        "combobox-entry-focused",
        "entry-focused",
        "entry-toolbar-focused",
        "progressbar-horizontal-fill",
        "progressbar-vertical-fill",
        "radiance-button-toolbar-active-focused",
        "radiance-button-toolbar-focused",
        "radiance-combobox-button-toolbar-focused",
        "radiance-entry-toolbar-focused",
        "radio-selected",
        "scale-horizontal-fill",
        "scale-vertical-fill",
        "slider-horizontal-focused",
        "slider-horizontal-focused-hover",
        "slider-vertical-focused",
        "slider-vertical-focused-hover",
        "switch-button-on",
        "switch-trough-focused",
        "switch-trough-on",
        "switch-trough-toolbar-on",
    ]:
        for gtk_dir in ["gtk-2.0", "gtk-3.0", "gtk-3.20"]:
            for suffix in [".png", "@2.png"]:
                cur_dir = os.path.join(prop.target_dir_theme, gtk_dir, "assets")
                filename = asset + suffix

                if not os.path.exists(cur_dir):
                    continue
                os.chdir(cur_dir)

                if not os.path.exists(filename):
                    continue

                # Convert icon to grey and colourise
                colourize_raster(prop.new_hex_value, filename)

    print("\nTheme assets generated.\n")


def patch_icons():
    """
    Search through the icons and replace green with new values.
    """
    os.chdir(os.path.realpath(prop.target_dir_icons))

    if not prop.build_icons:
        return

    print("Patching icons...")

    # --> Metadata
    replace_string("index.theme", "Name=" + prop.base_icon_theme, "Name=" + prop.new_icon_name)

    replace_string("index.theme", "Inherits=ubuntu-mono-dark,", "Inherits=ubuntu-mono-dark,{0},".format(prop.base_icon_theme))
    replace_string("index.theme", "Inherits=ubuntu-mono-light,", "Inherits=ubuntu-mono-light,{0},".format(prop.base_icon_theme))

    # --> General colours and shades
    replace_string("*.svg", "#87A752", prop.new_hex_value) # <= 19.10
    replace_string("*.svg", "#87A556", prop.new_hex_value) # >= 20.04 (Official)
    replace_string("*.svg", "#ADC980", get_hex_variant(prop.new_hex_value, 16))
    replace_string("*.svg", "#688933", get_hex_variant(prop.new_hex_value, -12))
    replace_string("*.svg", "#4e7752", get_hex_variant(prop.new_hex_value, -10))
    replace_string("*.svg", "#4A6A17", get_hex_variant(prop.new_hex_value, -24))

    #--> actions (go-home)
    replace_string("*.svg", "#d9edb9", get_hex_variant(prop.new_hex_value, 34))
    replace_string("*.svg", "#f6daae", get_hex_variant(prop.new_hex_value, 33))

    # --> preferences-desktop-theme
    replace_string("*.svg", "#4e6827", get_hex_variant(prop.new_hex_value, -21))
    replace_string("*.svg", "#617f30", get_hex_variant(prop.new_hex_value, -15))
    replace_string("*.svg", "#87a556", get_hex_variant(prop.new_hex_value, -1))
    replace_string("*.svg", "#b4c990", get_hex_variant(prop.new_hex_value, 19))

    # --> preferences-system-network
    replace_string("*.svg", "#4d5e31", get_hex_variant(prop.new_hex_value, -21))
    replace_string("*.svg", "#abc187", get_hex_variant(prop.new_hex_value, 15))
    replace_string("*.svg", "#657b40", get_hex_variant(prop.new_hex_value, -12))
    replace_string("*.svg", "#4a5a2f", get_hex_variant(prop.new_hex_value, -22))

    #--> system-file-manager
    replace_string("*.svg", "#2e4705", get_hex_variant(prop.new_hex_value, -34))

    # --> home
    replace_string("*.svg", "#3b550e", get_hex_variant(prop.new_hex_value, -30))

    print("Icons patched.\n")


# ------------------------------------------------
# Optional Tweaks
# ------------------------------------------------
class Tweaks(object):
    """
    Performs some modifications that are different to the original theme/icons
    or compliments the newly generated colour theme/icons.
    """
    def __init__(self):
        """
        Stores a list of optional tweaks to perform in addition to the colours.

        "tweak_id": [<function>, "description"]
        """
        self.tweaks = {
            "mono-osd-icons": [self.mono_osd_icons, "Use mono icons for the OSD volume pop up"],
            "black-selected-text": [self.black_selected_text, "Change the selected text colour to black."],
            "gtk3-classic": [self.gtk3_classic_extras, "Additional styling for gtk3-classic package"],
        }

    def perform_tweaks(self):
        """
        Run through the tweaks, if any.
        """
        for tweak in prop.tweaks:
            print("\nApplying tweak: " + tweak)
            self.tweaks[tweak][0]()

    def mono_osd_icons(self):
        """
        Use the monochrome icons for the volume pop-up that's been used for years (#14)

        This was changed upstream (ubuntu-mate-artwork) as the icon interfered
        with some apps, so this restores the monochrome icon which will
        be used in the OSD.
        """
        if not prop.build_icons:
            return

        os.chdir(os.path.join(prop.target_dir_icons, "status", "24"))
        for path in [
            ["audio-volume-high-panel.svg", "audio-volume-high.svg"],
            ["audio-volume-medium-panel.svg", "audio-volume-medium.svg"],
            ["audio-volume-low-panel.svg", "audio-volume-low.svg"],
            ["audio-volume-muted-panel.svg", "audio-volume-muted.svg"]
        ]:
            if os.path.exists(path[1]):
                os.remove(path[1])
            os.symlink(path[0], path[1])

    def black_selected_text(self):
        """
        All the themes originally use a white selected text colour. This inverts
        the selected text colour to black to improve contrast.
        """
        os.chdir(prop.target_dir_theme)

        # Ambiant/Radiant
        replace_string(["*.ini", "gtkrc"], "selected_fg_color:#ffffff", "selected_fg_color:#000000")
        replace_string("*.css", "selected_fg_color #ffffff", "selected_fg_color #000000")

        # Ambiant-Dark
        replace_string(["*.ini", "gtkrc"], "selected_fg_color:#EBEBEB", "selected_fg_color:#000000")
        replace_string("*.css", "selected_fg_color #EBEBEB", "selected_fg_color #000000")

        # Remove shadow when hovering over menus - escaped for regex
        replace_string("*.css", "text-shadow: 0 -1px shade \(\@selected_bg_color, 0\.7\)", "text-shadow: none")

    def gtk3_classic_extras(self):
        """
        Adds additional CSS for convenience with gtk3-classic, such as
        alternating treeview rows.
        """
        if not prop.build_theme:
            return

        os.chdir(prop.target_dir_theme)
        with open("gtk-3.0/gtk.css", "a") as f:
            f.write("\n@import url(\"gtk3-classic.css\");")

        orig = os.path.join(prop.templates_dir, "gtk3-classic.css")
        dest = os.path.join(prop.target_dir_theme, "gtk-3.0", "gtk3-classic.css")
        shutil.copy(orig, dest)


# ------------------------------------------------
# Miscellaneous
# ------------------------------------------------
def colour_wallpapers():
    """
    Create colourised versions of the common Ubuntu MATE wallpapers.
    """
    if not prop.build_wallpapers:
        return

    wallpapers_src = [
        [
            "usr/share/backgrounds/ubuntu-mate-common/Green-Jazz.jpg",
            prop.new_name + " Ubuntu MATE Jazz",
            "Roberto Perico"
        ],
        [
            "usr/share/backgrounds/ubuntu-mate-common/Green-Wall-Logo-Text.png",
            prop.new_name + " Wall (Logo and Text)",
            "Roberto Perico"
        ],
        [
            "usr/share/backgrounds/ubuntu-mate-common/Green-Wall-Logo.png",
            prop.new_name + " Wall (Logo)",
            "Roberto Perico"
        ],
        [
            "usr/share/backgrounds/ubuntu-mate-common/Green-Wall.png",
            prop.new_name + " Wall",
            "Roberto Perico"
        ],
        [
            "usr/share/backgrounds/ubuntu-mate-common/Ubuntu-MATE-Splash.jpg",
            prop.new_name + " Ubuntu MATE Splash",
            "Martin Wimpress"
        ]
    ]

    print("Generating wallpapers...")

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!DOCTYPE wallpapers SYSTEM "mate-wp-list.dtd">',
        '<wallpapers>'
    ]

    for wallpaper in wallpapers_src:
        path = wallpaper[0]
        display_name = wallpaper[1]
        artist = wallpaper[2]

        original = os.path.realpath(os.path.join(prop.src_path, path))
        new_filename = os.path.basename(os.path.splitext(original)[0]).replace("Green", prop.new_name) + os.path.splitext(original)[1]

        tmp_path = os.path.join("/tmp/" + new_filename)
        new_path = os.path.join(prop.target_dir_wallpapers, new_filename)

        if not os.path.exists(original):
            print("\nWallpaper no longer exists: " + original)
            exit(1)

        print("Generating:", new_path)

        os.system("convert {input} -colorspace gray {output}".format(input=original, output=tmp_path))
        if not os.path.exists(tmp_path):
            print("\nFailed to generate: " + tmp_path)
            exit(1)

        os.system("convert {input} -background white -fill '{hex}' -tint 100 {output}".format(input=tmp_path, hex=prop.new_hex_value, output=new_path))
        if not os.path.exists(new_path):
            print("\nFailed to generate: " + new_path)
            exit(1)

        # Clean up temporary files
        os.remove(tmp_path)

        # Add wallpaper to XML file
        if prop.packaging:
            new_path = "/usr/share/backgrounds/ubuntu-mate-colours-{colour}/{filename}".format(
                colour=prop.new_name.lower(),
                filename=new_filename)

        xml.append('    <wallpaper deleted="false">'),
        xml.append('      <name>' + display_name + '</name>')
        xml.append('      <filename>' + new_path + '</filename>')
        xml.append('      <options>zoom</options>')
        xml.append('      <artist>' + artist + '</artist>')
        xml.append('    </wallpaper>')

    # Finish XML output
    xml.append('</wallpapers>')
    with open(prop.target_wallpapers_xml, "w") as f:
        f.writelines("\n".join(xml))

    print("Wallpaper generation complete.")


def generate_plank_theme():
    """
    Create a new theme file for the Plank dock.
    """
    if not prop.build_theme:
        return

    print("\nGenerating Plank theme...")
    template = os.path.join(prop.templates_dir, "plank.theme")

    shutil.copy(template, prop.target_plank_theme)

    # The template uses RRR, GGG and BBB as placeholders.
    with open(template, "r") as f:
        lines = f.readlines()

    rgb = hex_to_rgb_list(prop.new_hex_value)
    output = []
    for line in lines:
        if line.find("RR"):
            line = line.replace("RRR;;GGG;;BBB", "{0};;{1};;{2}".format(rgb[0], rgb[1], rgb[2]))

        output.append(line)

    with open(prop.target_plank_theme, "w") as f:
        f.writelines(output)

    print("Plank theme created.\n")


# ------------------------------------------------
# Showtime!
# ------------------------------------------------
if __name__ == "__main__":

    # Check required external software is installed
    if not shutil.which("rsvg-convert"):
        print("'rsvg-convert' command not found. Please install 'librsvg2-bin'")
        exit(1)

    if not shutil.which("convert"):
        print("'convert' command not found. Please install 'imagemagick'")
        exit(1)

    prop = Properties()
    tweaks = Tweaks()
    parse_arguments()

    # Output summary of what's going to happen.
    print("\nNew variant to be generated:\n")
    print("           Hex Value: " + prop.new_hex_value)
    if prop.build_theme:
        print("           New Theme: " + prop.new_theme_name)
    if prop.build_icons:
        print("           New Icons: " + prop.new_icon_name)
    print("              Source: " + prop.src_path)
    print("   /usr/share prefix: " + prop.target_share_path)
    if prop.build_theme:
        print("    Install theme to: " + prop.target_dir_theme)
    if prop.build_icons:
        print("    Install icons to: " + prop.target_dir_icons)
    if prop.build_wallpapers:
        print("   New wallpapers to: " + prop.target_dir_wallpapers)
    if len(prop.tweaks) > 0:
        print("              Tweaks: " + ", ".join(prop.tweaks))
    print("")

    # Perform the changes
    prep_targets()
    patch_theme()
    patch_icons()
    optimise_icon_size(prop.src_path + "/usr/share/icons/" + prop.base_icon_theme, prop.target_dir_icons)
    colour_wallpapers()
    generate_plank_theme()
    tweaks.perform_tweaks()

    print("\nGeneration of theme '{0}' complete.".format(prop.new_theme_name))
    exit(0)
