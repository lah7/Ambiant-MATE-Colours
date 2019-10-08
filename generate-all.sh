#!/bin/bash
#
# Generates all the themes - for packaging use only!
#
CUR=0
TOTAL=$(( 10 * 3 ))

# Clear out existing files first
if [ -d usr/share/icons ]; then
    rm -r usr/share/icons
fi

if [ -d usr/share/themes ]; then
    rm -r usr/share/themes
fi

function generate() {
    theme="$1"
    hex="$2"
    name="$3"
    CUR=$(( CUR + 1 ))
    echo "Generating $CUR of $TOTAL..."
    echo "=================================================="

    ./ubuntu-mate-colours-generator \
        --overwrite \
        --ignore-existing \
        --install-icon-dir=usr/share/icons \
        --install-theme-dir=usr/share/themes \
        --src-dir=/ \
        --theme="$theme" \
        --hex="$hex" \
        --name="$name"
}

for theme in "Ambiant-MATE" "Ambiant-MATE-Dark" "Radiant-MATE"; do
    generate "$theme" "#2DACD4" "Aqua"
    generate "$theme" "#5489CF" "Blue"
    generate "$theme" "#7F441F" "Brown"
    generate "$theme" "#679816" "Green"
    generate "$theme" "#E66C1E" "Orange"
    generate "$theme" "#E231A3" "Pink"
    generate "$theme" "#7E5BC5" "Purple"
    generate "$theme" "#CE3A3A" "Red"
    generate "$theme" "#1CB39F" "Teal"
    generate "$theme" "#D8A200" "Yellow"
done
