#!/bin/bash
#
# Build the Debian package, usually performed by Launchpad.
#
# =======================
# For packaging use only!
# =======================
#
# Ambiant-MATE Family:
#   - Generate each variant using 'ubuntu-mate-colours-generator'
#
CUR=0
TOTAL=$(( 9 * 3 ))

# Clear out any existing build
if [ -d usr/share ]; then
    rm -r usr/share/icons
fi

# Output package versions being processed
echo -e "\n=================================================="
echo "Versions"
echo "=================================================="
echo -n "Theme " && apt-cache show ubuntu-mate-themes | grep Version
echo -n "Icon Theme " && apt-cache show ubuntu-mate-icon-themes | grep Version
echo -n "Wallpaper " && apt-cache show ubuntu-mate-wallpapers-common | grep Version
echo -n "Meson " && apt-cache show meson | grep Version
echo -n "sassc " && apt-cache show sassc | grep Version

function generate_ambiant() {
    theme="$1"
    hex="$2"
    name="$3"
    tweaks="$4"
    CUR=$(( CUR + 1 ))
    echo -e "\n=================================================="
    echo "($CUR/$TOTAL) - $theme ($name, $hex)"
    echo "=================================================="

    ./ubuntu-mate-colours-generator \
        --overwrite \
        --ignore-existing \
        --install-icon-dir=usr/share/icons \
        --install-theme-dir=usr/share/themes \
        --install-wallpapers-dir=usr/share/backgrounds \
        --install-share-dir=usr/share \
        --src-dir=/ \
        --theme="$theme" \
        --hex="$hex" \
        --name="$name" \
        --tweaks=$tweaks \
        --packaging

    if [ $? != 0 ]; then
        echo "Build failed!"
        exit 1
    fi
}

for theme in "Ambiant-MATE" "Ambiant-MATE-Dark" "Radiant-MATE"; do
    #                 Hex #     Name     Tweaks
    #                 --------- -------- -------------------------------------
    generate_ambiant "$theme" "#2DACD4" "Aqua"   "mono-osd-icons"
    generate_ambiant "$theme" "#5489CF" "Blue"   "mono-osd-icons"
    generate_ambiant "$theme" "#965024" "Brown"  "mono-osd-icons"
    generate_ambiant "$theme" "#E95420" "Orange" "mono-osd-icons"
    generate_ambiant "$theme" "#E231A3" "Pink"   "mono-osd-icons"
    generate_ambiant "$theme" "#7E5BC5" "Purple" "mono-osd-icons"
    generate_ambiant "$theme" "#CE3A3A" "Red"    "mono-osd-icons"
    generate_ambiant "$theme" "#1CB39F" "Teal"   "mono-osd-icons"
    generate_ambiant "$theme" "#DFCA25" "Yellow" "mono-osd-icons,black-selected-text"
done

