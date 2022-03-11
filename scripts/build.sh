#!/bin/bash
#
# =======================
# For packaging use only!
# =======================
#
# Builds all the colour themes for the Debian package. Launchpad would normally
# run this script.
#
CUR=0
TOTAL=$(( 9 * 4 ))

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

    ./generate-ambiant-mate-colour.py \
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

function build_yaru() {
    hex="$1"
    name="$2"
    CUR=$(( CUR + 1 ))
    echo -e "\n=================================================="
    echo "($CUR/$TOTAL) - Yaru-MATE ($name, $hex)"
    echo "=================================================="

    ./generate-yaru-mate-colour.py \
        --hex "$hex" \
        --name "$name" \
        --src-dir yaru-src/ \
        --usr-dir usr/

    if [ $? != 0 ]; then
        echo "Build failed!"
        exit 1
    fi
}

for theme in "Ambiant-MATE" "Ambiant-MATE-Dark" "Radiant-MATE"; do
    #                 Hex #     Name     Tweaks
    #                 --------- -------- -------------------------------------
    generate_ambiant "$theme" "#2DACD4" "Aqua"   "gtk3-classic,mono-osd-icons"
    generate_ambiant "$theme" "#5489CF" "Blue"   "gtk3-classic,mono-osd-icons"
    generate_ambiant "$theme" "#965024" "Brown"  "gtk3-classic,mono-osd-icons"
    generate_ambiant "$theme" "#E95420" "Orange" "gtk3-classic,mono-osd-icons"
    generate_ambiant "$theme" "#E231A3" "Pink"   "gtk3-classic,mono-osd-icons"
    generate_ambiant "$theme" "#7E5BC5" "Purple" "gtk3-classic,mono-osd-icons"
    generate_ambiant "$theme" "#CE3A3A" "Red"    "gtk3-classic,mono-osd-icons"
    generate_ambiant "$theme" "#1CB39F" "Teal"   "gtk3-classic,mono-osd-icons"
    generate_ambiant "$theme" "#DFCA25" "Yellow" "gtk3-classic,mono-osd-icons,black-selected-text"
done

# Build Yaru-MATE variants
build_yaru "#2DACD4" "Aqua"
build_yaru "#5489CF" "Blue"
build_yaru "#965024" "Brown"
build_yaru "#E95420" "Orange"
build_yaru "#E231A3" "Pink"
build_yaru "#7E5BC5" "Purple"
build_yaru "#CE3A3A" "Red"
build_yaru "#1CB39F" "Teal"
build_yaru "#DFCA25" "Yellow"
