#!/bin/bash
#
# Generates all the themes - for packaging use only!
#
# The package needs to be generated on the latest Ubuntu, and then have the
# copy the binaries backported to older releases.
#
CUR=0
TOTAL=$(( 9 * 3 ))

# Clear out any existing build
if [ -d usr/share/icons ]; then
    rm -r usr/share/icons
fi

if [ -d usr/share/themes ]; then
    rm -r usr/share/themes
fi

if [ -d usr/share/backgrounds ]; then
    rm -r usr/share/backgrounds
fi

# Show versions of packages being processed
echo -e "\n=================================================="
echo "Versions"
echo "=================================================="
echo -n "Theme " && apt-cache show ubuntu-mate-icon-themes | grep Version
echo -n "Icon Theme " && apt-cache show ubuntu-mate-themes | grep Version
echo -n "Wallpaper " && apt-cache show ubuntu-mate-wallpapers-common | grep Version

function generate() {
    theme="$1"
    hex="$2"
    name="$3"
    tweaks="$4"
    CUR=$(( CUR + 1 ))
    echo -e "\n=================================================="
    echo "Generating $CUR of $TOTAL..."
    echo "=================================================="

    ./ubuntu-mate-colours-generator \
        --overwrite \
        --ignore-existing \
        --install-icon-dir=usr/share/icons \
        --install-theme-dir=usr/share/themes \
        --install-wallpapers-dir=usr/share/backgrounds \
        --install-wallpapers-xml-dir=usr/share/mate-background-properties \
        --src-dir=/ \
        --theme="$theme" \
        --hex="$hex" \
        --name="$name" \
        --tweaks=mono_osd_icons \
        --packaging

    if [ $? != 0 ]; then
        echo "Build unsuccessful!"
        exit 1
    fi
}

for theme in "Ambiant-MATE" "Ambiant-MATE-Dark" "Radiant-MATE"; do
    generate "$theme" "#2DACD4" "Aqua"
    generate "$theme" "#5489CF" "Blue"
    generate "$theme" "#965024" "Brown"
    generate "$theme" "#E95420" "Orange"
    generate "$theme" "#E231A3" "Pink"
    generate "$theme" "#7E5BC5" "Purple"
    generate "$theme" "#CE3A3A" "Red"
    generate "$theme" "#1CB39F" "Teal"
    generate "$theme" "#DFCA25" "Yellow"
done
