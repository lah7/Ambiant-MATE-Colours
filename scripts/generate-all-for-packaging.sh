#!/bin/bash
#
# Generates all the themes - for packaging use only!
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

# Ensure a copy of the latest ubuntu-mate-artwork
git clone "https://github.com/ubuntu-mate/ubuntu-mate-artwork.git" --depth=1 ubuntu-mate-artwork-src

function generate() {
    theme="$1"
    hex="$2"
    name="$3"
    CUR=$(( CUR + 1 ))
    echo -e "\n=================================================="
    echo "Generating $CUR of $TOTAL..."
    echo "=================================================="

    ./ubuntu-mate-colours-generator \
        --overwrite \
        --ignore-existing \
        --install-icon-dir=usr/share/icons \
        --install-theme-dir=usr/share/themes \
        --src-dir=ubuntu-mate-artwork-src/ \
        --theme="$theme" \
        --hex="$hex" \
        --name="$name"

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

# Clean up
rm -rf ubuntu-mate-artwork-src
